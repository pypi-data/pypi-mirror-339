#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  RRN_attention.py
#
#  Copyright 2019 Gabriel Orlando <orlando.gabriele89@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import warnings
warnings.filterwarnings("ignore")
import transformers
from torch import nn
import torch as t
import os

class NN_Single(nn.Module):

	def __init__(self, dev=t.device('cpu')):
		super(NN_Single, self).__init__()

		hidden_size = 50

		configCodonBert = transformers.BertConfig(vocab_size=130,
												  hidden_size=hidden_size,
												  num_hidden_layers=5,
												  num_attention_heads=5,
										 		  intermediate_size=100,
												  hidden_act='gelu',
												  hidden_dropout_prob=0.2,
										 		  attention_probs_dropout_prob=0.2,
												  max_position_embeddings=1024,
												  model_type="bert",
										 		  type_vocab_size=2,
												  initializer_range=0.02,
												  layer_norm_eps=1e-12,
										 		  pad_token_id=0,
												  )


		self.bert = transformers.BertModel(configCodonBert)

		self.dropout=nn.Dropout(0.0)

		self.final = nn.Sequential(nn.Linear(hidden_size,1),
								   nn.Sigmoid(),
								  )
	def load(self):
		file_path = "/".join(os.path.realpath(__file__).split("/")[:-1])+"/../"
		self.bert = transformers.BertModel.from_pretrained(file_path+"marshalled/final_modelBert.hugg_m")
		self.final.load_state_dict(t.load(file_path+"marshalled/final_modelFinalLayer.stateDict"))

	def forward(self, x,attention_mask=None):

		if attention_mask is None:
			attention_mask = x != 0

		pooled_output = self.dropout(self.bert(x,attention_mask, output_hidden_states=True)[1])

		logits = self.final(pooled_output)

		return logits.squeeze(1)

