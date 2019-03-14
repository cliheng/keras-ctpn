# -*- coding: utf-8 -*-
"""
   File Name：     detector
   Description :   文本行检测器
   Author :       mick.yi
   date：          2019/3/14
"""
import numpy as np
from .text_proposal_connector import TextProposalConnector
from ..utils import np_utils


class TextDetector:
    """
        Detect text from an image
    """

    def __init__(self, config):
        self.config = config
        self.text_proposal_connector = TextProposalConnector()

    def detect(self, text_proposals, scores, image_shape):
        """

        :param text_proposals: 文本提议框
        :param scores: 文本框得分
        :param image_shape: 图像形状
        :return: text_lines; [ num,(y1,x1,y2,x2,score)]
        """

        # scores = normalize(scores)

        text_lines = self.text_proposal_connector.get_text_lines(text_proposals, scores, image_shape)
        keep_indices = self.filter_boxes(text_lines)
        text_lines = text_lines[keep_indices]

        # nms for text lines
        if text_lines.shape[0] != 0:
            keep_indices = np_utils.non_max_suppression(text_lines[:, :4], text_lines[:, 4],
                                                        self.config.TEXT_LINE_NMS_THRESH)
            text_lines = text_lines[keep_indices]

        return text_lines

    def filter_boxes(self, boxes):
        heights = boxes[:, 2] - boxes[:, 0]
        widths = boxes[:, 3] - boxes[:, 1]
        scores = boxes[:, -1]
        return np.where((widths / heights > self.config.MIN_RATIO) & (scores > self.config.LINE_MIN_SCORE) &
                        (widths > (self.config.TEXT_PROPOSALS_WIDTH * self.config.MIN_NUM_PROPOSALS)))[0]
