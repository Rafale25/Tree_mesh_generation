import random
import math

import glm

from utils import *

class TreeNode:
    def __init__(self, parent, pos, depth):
        self.pos = glm.vec3(pos)
        self.pos_smooth = glm.vec3(pos)

        self.radius = max(0.02, 0.2 - depth*0.002)
        # self.radius = 0.04
        self.depth = depth #how many nodes from root

        self.parent = parent
        self.childs = []

    def length(self):
        return glm.distance(self.pos, self.parent.pos)

    def __str__(self):
        return "[{}: {}]".format(self.pos, self.childs)

class Tree:
    MAX_LEN = 2.0
    MAX_DEPTH = 20
    MAX_DIVISION_DEPTH = 20
    MIN_CHILDS = 1
    MAX_CHILDS = 1
    NB_SEGMENTS = 8
    NB_FACES = 8

    def __init__(self):
        self.root = TreeNode(parent=None, pos=glm.vec3(0, 0, 0), depth=0)
        self.nodes = [] #[TreeNode]

    def __str__(self):
        return "\n".join(str(node) for node in self.nodes)

    def size(self):
        return len(self.nodes)

    def clear(self):
        self.root = TreeNode(parent=None, pos=glm.vec3(0, 0, 0), depth=0)
        self.nodes = [] #[TreeNode]
        self.nodes.append(TreeNode(parent=self.root, pos=glm.vec3(1, 1, 0), depth=1))

    def update(self):
        speed = 0.05
        for node in self.nodes:
            node.pos_smooth = node.pos_smooth + (node.pos - node.pos_smooth) * speed

    def grow(self):
        for node in self.nodes:
            if len(node.childs) > 0 and node.length() >= Tree.MAX_LEN:
                continue

            if node.length() < Tree.MAX_LEN:
                dir = glm.normalize(glm.sub(node.pos, node.parent.pos))
                node.pos += dir * 0.01
            else:
                nb_childs = random.randint(Tree.MIN_CHILDS, Tree.MAX_CHILDS)

                if node.depth > Tree.MAX_DIVISION_DEPTH:
                    nb_childs = 1
                if node.depth > Tree.MAX_DEPTH:
                    continue

                offset = random_uniform_vec3() * 0.1
                # offset.y = math.fabs(offset.y)

                for i in range(nb_childs):
                    new_child_node = TreeNode(parent=node, pos=node.pos + offset, depth=node.depth+1)
                    node.childs.append(new_child_node)
                    self.nodes.append(new_child_node)
