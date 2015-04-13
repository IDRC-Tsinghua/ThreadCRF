#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

# TODO: Supplement the three emoji lists
positiveEmoji = ['[哈哈]', '[偷笑]', '[嘻嘻]', '[爱你]', '[心]', '[挤眼]', '[抱抱]',
                 '[鼓掌]', '[good]', '[花心]', '[赞]', '[给力]', '[酷]', '[害羞]', '[威武]',
                 '[可爱]', '[兔子]', '[太开心]', '[耶]', '[亲亲]', '[蛋糕]', '[笑哈哈]', '[撒花]',
                 '[可怜]', '[羊年大吉]', '[江南style]', '[偷乐]', '[得意地笑]', '[笑cry]',
                 '[馋嘴]', '[钱]', '[互粉]', '[ok]', '[礼物]', '[求关注]', '[好爱哦]', '[噢耶]']
neutralEmoji = ['[doge]', '[泪]', '[呵呵]', '[阴险]', '[话筒]']
negativeEmoji = ['[抓狂]', '[挖鼻屎]', '[汗]', '[衰]', '[怒]', '[晕]', '[生病]', '[哼]',
                 '[委屈]', '[鄙视]', '[泪流满面]', '[肥皂]', '[闭嘴]', '[懒得理你]', '[左哼哼]', '[右哼哼]',
                 '[嘘]', '[吐]', '[打哈气]', '[拜拜]', '[困]', '[失望]', '[悲伤]', '[黑线]',
                 '[怒骂]', '[不要]', '[弱]', '[草泥马]', '[囧]', '[蜡烛]', '[巨汗]', '[崩溃]']


def getEmojiLabel(emoji):
    if emoji.encode('utf-8') in positiveEmoji:
        return 1
    elif emoji.encode('utf-8') in neutralEmoji:
        return 0
    elif emoji.encode('utf-8') in negativeEmoji:
        return -1
    else:
        return 0
