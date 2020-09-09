# -*-coding:utf-8-*-

from py2neo import Graph, Node, Relationship

# 连接neo4j数据库，输入地址、用户名、密码
test_graph = Graph('http://192.168.1.98:7474')

# 初始化
test_graph.run('MATCH (n:`人`)-[r]-() delete r')
test_graph.run('MATCH (n:`人`) delete n')

# 建立节点
test_node_1 = Node("人", name="小明")
test_node_2 = Node("人", name="小红")
test_graph.create(test_node_1)
test_graph.create(test_node_2)

# 建立关系
node_1_call_node_2 = Relationship(test_node_1, '喜欢', test_node_2)
# node_1_call_node_2['count'] = 1
node_2_call_node_1 = Relationship(test_node_2, '讨厌', test_node_1)
# node_2_call_node_1['count'] = 2
test_graph.create(node_1_call_node_2)
test_graph.create(node_2_call_node_1)

# 删
test_node_3 = Node("人", name="小刚")
test_graph.create(test_node_3)
test_graph.delete(test_node_3)

# 改
test_node_2['age'] = 20
test_graph.push(test_node_2)

test_node_2['age'] = 22
test_graph.push(test_node_2)

node_1_call_node_2['程度'] = '非常'
test_graph.push(node_1_call_node_2)

# 查
data1 = test_graph.run('MATCH (a:人) RETURN a')

data = test_graph.run('MATCH (a:人) RETURN a').data()

node_ids = []
new_nodes = []
new_links = []

for a in data:
    for tk, tv in a.items():
        nodes = tv.nodes
        relations = tv.relationships
        for n in nodes:
            if n.identity in node_ids:
                continue
            obj = {}
            obj["id"] = n.identity
            obj["label"] = []
            if n.labels is not None:
                for la in n.labels:
                    obj["label"].append(la)
            for k, v in n.items():
                obj[k] = v
            node_ids.append(n.identity)
            new_nodes.append(obj)
        for r in relations:
            if r.identity in node_ids:
                continue
            li = {}
            li["id"] = r.identity
            if r.types() is not None:
                li["label"] = []
                for la in r.types():
                    li["label"].append(la)
            li["source"] = r.start_node.identity
            li["target"] = r.end_node.identity
            for k,v in r.items():
                li[k] = v
            node_ids.append(r.identity)
            new_links.append(li)
result = {}
result["nodes"] = new_nodes
result["links"] = new_links
# Unicode 转换到汉字就行了
print(result)


