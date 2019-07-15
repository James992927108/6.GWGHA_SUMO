from xml.etree import ElementTree as ET
import random


def get_total_id_list(root):
    total_id_list = []
    for child in root.iter('vehicle'):
        if child.get('id') > 0:
            # print child.get('id')
            total_id_list.append(int(child.get('id')))
    return total_id_list
    

filename = "map.rou.xml"
select_id_nmuber = 500

tree = ET.parse(filename)
root = tree.getroot()
total_id_list = get_total_id_list(root)
random_id_list = sorted(random.sample(total_id_list, select_id_nmuber))

print len(random_id_list)

total = 0
for index, child in enumerate(root.iter('vehicle')):
    if int(child.get('id')) in random_id_list:
        if int(child.get('id')) != index:
            print "---"
            print index , child.get('id')
            child.set('id', str(index))
            print index , child.get('id')
        total += 1
    else:
        root.remove(child)
print total

tree.write(filename)