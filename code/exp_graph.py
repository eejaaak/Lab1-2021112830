import networkx as nx
import matplotlib.pyplot as plt
import random
import os
import re

def get_path(address):
    current_directory = os.getcwd()
    if address.startswith(current_directory):
        return address

    file_path = os.path.join(current_directory,address)
    return file_path

address = input('文本地址为：')
input_file_path = get_path(address)


# 图的实现方式：每个顶点存储一个字符串，以及它邻接到的所有顶点，及其权值
class Vertex:
    def __init__(self, key, value=''):
        self.key = key  # 顶点的序号
        self.value = value  # 存储一个字符串
        self.neighbors = {}  # 以词典形式，存储它邻接到的顶点，键为其所有邻接到的顶点，值为权值（词语的邻接次数）
        self.edge_flag = {}
        self.flag = False
    def add_neighbor(self, neighbor):
        if neighbor in self.neighbors:
            self.neighbors[neighbor] += 1  # 如果邻接点已存在，则权值加1
        else:
            self.neighbors[neighbor] = 1  # 否则，初始化权值为1
            self.edge_flag[neighbor] = 0


# 读取文件并创建一个空的有向图
def create_graph(filepath):
    vertices = {}  # 以词典形式，所有顶点，键为其单词字符串，值为顶点
    former_word = None

    with open(filepath, 'r') as file:
        word_index = 4
        for line in file:
            words = line.split()  # 分割单词
            for word in words:
                word = re.sub(r'[^a-zA-Z]', '', word)  # 去掉标点符号
                if word:  # 非空
                    if word not in vertices:  # 建立新的节点
                        vertices[word] = Vertex(word_index, word)
                        word_index += 1
                    if former_word is not None:  # 第一个单词的处理
                        vertices[former_word].add_neighbor(vertices[word])
                    former_word = word

    return vertices


def create_present_graph(vertices):
    G = nx.DiGraph()

    # 将顶点和边添加到有向图中
    for key, vertex in vertices.items():
        G.add_node(vertex.key, label=vertex.value)

    for vertex in vertices.values():
        for neighbor, weight in vertex.neighbors.items():
            G.add_edge(vertex.key, neighbor.key, weight=weight)

    # 绘制有向图
    pos = nx.spring_layout(G)  # 为图形选择布局
    labels = nx.get_node_attributes(G, 'label')
    edge_labels = {(n1, n2): G[n1][n2]['weight'] for n1, n2 in G.edges}
    nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=200, font_weight='bold', font_size=10, arrowsize=20, arrowstyle='->',connectionstyle='arc3, rad = 0.1')
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)这里的有向边的权值显示有bug，故注释掉
    plt.show()#会一直保持，直到关闭

    return

def find_bridges(vertices):
    word1 = input("first word:")
    word2 = input("second word:")
    bridges = []
    if( word1 not in vertices or word2 not in vertices):
        print("No word1 or word2 not in the graph")
        return None

    for b_neighbor in vertices[ word1 ].neighbors:
        for v2 in b_neighbor.neighbors:
            if v2 == vertices[ word2 ]:
                bridges.append( b_neighbor.value )
            else:
                print("No Bridge Words from ,, to,,")
                return None
    print("The bridge words from word1 to word2 are:"  )
    for str in bridges:
        print(str)

    return bridges

def find_bridges1(word1, word2, vertices):

    bridges = []
    if( word1 not in vertices and word2 not in vertices):
        # print("No word1 or word2 i the graph")
        return None

    for b_neighbor in vertices[ word1 ].neighbors:
        for v2 in b_neighbor.neighbors:
            if v2 == vertices[ word2 ]:
                bridges.append( b_neighbor.value )

    # print("The bridge words from word1 to word2 are:"  )

    return bridges

def join_strings(sentence_list):
    return ' '.join(sentence_list)

def generate_new_text(vertices):
    word_text = input('输入新文本：')
    word_text = word_text.split()
    # print(word_text)
    for i in range(1,len(word_text)):
        if word_text[i-1] not in vertices or word_text[i] not in vertices:
            continue
        bridge = find_bridges1(word_text[i-1], word_text[i], vertices)
        if bridge:
            new_word = random.choice(bridge)
            word_text[i-1] += " " + new_word
    result_sentence = join_strings(word_text)
    print(result_sentence)


# def initiat_flag(vertices):
#     for v in vertices.values():
#         v.flag = False
#         for a in v.edge_flag.values():
#             a = 0

def initiat_flag(vertices):
    for v in vertices.values():
        v.flag = False
        for key in v.edge_flag:  # 遍历字典的键
            v.edge_flag[key] = 0  # 直接对字典值进行赋值

# 递归地访问有向图
def into_neigh(v1, weight, vpd, stack, shortest):
    # 已经访问的顶点
    if v1.flag == True:
        return

    # 入栈此节点
    stack.append(v1.value)

    if (v1 == vpd):
        # 判断目前为止的路径是否是最短路径，如果是则更新
        # print(stack)
        # print(weight)
        if (shortest[0] == None or stack[0] < shortest[0][0]):
            stack[0] = weight
            shortest[0] = stack.copy()  # 拷贝栈到最短路径

        # 出栈此节点
        stack.pop()
        return

    # 更新为已访问
    v1.flag = True

    # 依次访问邻居
    for neigh, weight0 in v1.neighbors.items():
        into_neigh(neigh, weight + weight0, vpd, stack, shortest)

    # 出栈此节点
    stack.pop()

    return

    pass


# 计算最短路径的函数
def calculate_shortest(vertices):
    initiat_flag(vertices)

    pass
    word1 = input("first word:")
    word2 = input("second word:")
    if (word1 not in vertices or word2 not in vertices):
        print("No word1 or word2 in the graph")
        return None

    stack = [0]  # 栈，保存当前节点的路径
    shortest = [None]  # 保存最小加权路径长的路径
    vp1 = vertices[word1]  # 起点
    vpd = vertices[word2]  # 目标

    into_neigh(vp1, 0, vpd, stack, shortest)

    # 打印最短路径
    if (shortest[0] == None):
        print("两个单词不可达")
    else:
        print(shortest[0][1], end="")
        for str0 in shortest[0][2:]:
            print(" -> ", end="")
            print(str0, end="")
        print(" \nwith weight of " + str(shortest[0][0]))

def into_node(node,stack):
    node.flag = True

    if not node.neighbors:
        stack = stack + [node.value]
        result_sentence = join_strings(stack)
        print(result_sentence)
        return stack

    i = random.choice(list(node.neighbors))
    stack.append(node.value)
    if node.edge_flag[i] == 1:
        stack = stack + [i.value]
        result_sentence = join_strings(stack)
        print(result_sentence)
        return stack
    node.edge_flag[i] = 1
    stack = into_node(i, stack)

    return stack



def random_walk(vertices):
    initiat_flag(vertices)
    node = random.choice(list(vertices.values()))
    stack = []
    stack = into_node(node,stack)
    # 将堆栈写入文件
    with open('random_walk_output.txt', 'w') as f:
        for item in stack:
            f.write("%s\n" % item)

def main(input_file_path):
    filepath = input_file_path
    vertices = create_graph(filepath)
    create_present_graph(vertices)


    while True:
        print("\n请选择要执行的操作：")
        print("1. 查询桥接词")
        print("2. 生成新文本")
        print("3. 计算最短路径")
        print("4. 随机游走")
        print("5. 退出程序")

        choice = input("请输入操作编号：")

        if choice == '1':
            find_bridges(vertices)
        elif choice == '2':
            generate_new_text(vertices)
        elif choice == '3':
            calculate_shortest(vertices)
        elif choice == '4':
            random_walk(vertices)
        elif choice == '5':
            print("感谢使用，再见！")
            break
        else:
            print("无效的操作编号，请重新输入。")


# 在这里调用 main 函数，并传入参数
if __name__ == "__main__":
    main(input_file_path)  # 传入示例文件路径
