#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

# TODO: Supplement the three emoji lists
positiveEmoji = ['[哈哈]', '[偷笑]']
neutralEmoji = ['[doge]']
negativeEmoji = ['[衰]']


def getEmojiLabel(emoji):
  if emoji in positiveEmoji:
    return 1
  elif emoji in neutralEmoji:
    return 0
  elif emoji in negativeEmoji:
    return -1
  else:
    return None
