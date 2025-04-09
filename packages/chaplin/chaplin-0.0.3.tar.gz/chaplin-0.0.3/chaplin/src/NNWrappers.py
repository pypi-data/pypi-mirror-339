#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
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

from sklearn.metrics import roc_auc_score
from torch import nn
import os, copy, random, time
from sys import stdout
import numpy as np
import torch as t
import torch
from transformers import TrainingArguments, Trainer
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader

from sklearn.preprocessing import QuantileTransformer
from chaplin.src import model

class NNwrapper():


	def __init__(self, device='cpu'):
		self.loss = torch.nn.BCELoss()

		self.tokenizerBERTCODON = self.get_tokenizer()
		self.model=model.NN_Single().to(device)

		self.device = device

	def load(self):
		self.model.load()
		file_path = "/".join(os.path.realpath(__file__).split("/")[:-1])+"/../"
		self.probability_scaler= torch.load(file_path+"marshalled/probability_scaler.m",weights_only=False)


	def get_tokenizer(self):
		from tokenizers import Tokenizer
		from tokenizers.models import WordLevel
		from tokenizers.pre_tokenizers import Whitespace
		from tokenizers.processors import BertProcessing
		"""Create tokenizer."""
		lst_ele = list("AUGCN")
		lst_voc = ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"]
		for a1 in lst_ele:
			for a2 in lst_ele:
				for a3 in lst_ele:
					lst_voc.extend([f"{a1}{a2}{a3}"])
		dic_voc = dict(zip(lst_voc, range(len(lst_voc))))
		tokenizer = Tokenizer(WordLevel(vocab=dic_voc, unk_token="[UNK]"))
		tokenizer.add_special_tokens(["[PAD]", "[CLS]", "[UNK]", "[SEP]", "[MASK]"])
		tokenizer.pre_tokenizer = Whitespace()
		tokenizer.post_processor = BertProcessing(
			("[SEP]", dic_voc["[SEP]"]),
			("[CLS]", dic_voc["[CLS]"]),
		)
		tokenizer.pad_token_id=dic_voc["[PAD]"]
		tokenizer.unk_token_id=dic_voc["[UNK]"]
		tokenizer.cls_token_id = dic_voc["[CLS]"]
		tokenizer.sep_token_id = dic_voc["[SEP]"]
		tokenizer.mask_token_id = dic_voc["[MASK]"]

		return tokenizer


	def collateFunction(self, batch):  # [(X[i], [task1, task2, ...]),... ]
		x = []
		y = []
		precalculatedBert=[]
		for i in range(len(batch)):
			x += [batch[i][0]]
			y += [batch[i][1].unsqueeze(0)]
			if len(batch[i])==3:
				precalculatedBert+=[batch[i][2]]
		y=torch.cat(y,dim=0)
		if precalculatedBert==[]:
			return x,y
		else:
			precalculatedBert = torch.cat(precalculatedBert,dim=0)
			return x,y,precalculatedBert
	def buildVector(self,inp):
		seqs=[]
		x=[]
		for prot in inp:
			seqs+=[" ".join(prot[:-1])]
			x+=[self.tokenizerBERTCODON.encode(" ".join(prot[:-1]).replace("T","U")).ids]
		return x

	class myDataset(Dataset):
		def __init__(self, X, Y = None,precalculatedBert = None):
			self.X=X
			self.Y=Y
			self.precalculatedBert = precalculatedBert
		def __len__(self):
			return len(self.X)
		def __getitem__(self, idx):
			o=[self.X[idx]]
			if self.Y is not None:
				o+=[self.Y[idx]]
			if self.precalculatedBert is not None:
				o += [self.precalculatedBert[idx]]
			return tuple(o)

	def __call__(self,x):
		return self.predict(x)
	def predict(self,X,scale_output=False):
		xvect = self.buildVector(X)
		self.model.eval()
		#self.model.training = False

		x=[]
		#padding_lens=[]
		sig = torch.nn.Sigmoid()

		for i in xvect:
			x+=[torch.tensor(i,dtype=torch.long,device=self.device)]
			#padding_lens+=[len(i)]
		x = pad_sequence(x, padding_value=0, batch_first=True).to(self.device).long()

		del xvect

		pred=[]
		dataset = self.myDataset(x)
		loader = DataLoader(dataset, batch_size=10, shuffle=False, sampler=None, num_workers=0)

		for sample in loader:
			xSamp = sample[0]
			attention_mask = xSamp != 0
			#xSamp = pad_sequence(xSamp, padding_value=0, batch_first=True).to(self.device).long()

			with torch.no_grad():

				yp = self.model(xSamp,attention_mask)
				pred += yp.cpu().data.tolist()
			
		if scale_output:
			pred = self.probability_scaler.transform(np.array(pred).reshape((-1,1))).reshape(-1)
		return pred



