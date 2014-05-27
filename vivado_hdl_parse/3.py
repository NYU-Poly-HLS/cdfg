import sys

if len(sys.argv) != 2:
    print("Usage: 3.py <filename>")
    sys.exit

fin = open(sys.argv[1], "r")
out = sys.argv[1]
#fin=open('dir.vhd','r')
#out='dir.vhd'
filename = out[: len(out) - 4] + ".txt"
fout = open(filename, "w")


entity_name = ''
e_array = []
port_list = []
signal_list = []
entity_find = 0
port_status = 0
signal_find = 0
process_find = 0
process_valid = 0
operator_count = 0
operator_array = ['+', '-', '*', '/', '<<', '>>']
operator_list = []
mux_list = []
condition_list = ['=', '>', '<']
line_extend = 0

class port():
    def __init__(self):
        self.name = ''
        self.types = ''
        self.width = ''
        self.direction = ''
        self.to = []
        self.sfrom = []
    def port_name(self, s):
            self.name = s
    def port_direction(self, s):
            self.direction = s
    def port_width(self, s):
            self.width = s
    def port_type(self, s):
            self.types = s
    def port_to(self, s):
            self.to.append(s)
    def port_from(self, s):
            self.sfrom.append(s)

class mux():
    def __init__(self):
        self.name = ''
        self.op1 = ''
        self.op2 = ''
        self.types = ''
        self.left_op = ''
        self.right_op = ''
        self.to = ''
        self.sfrom = []
    def mux_name(self, s):
        self.name = s
    def mux_op1(self, s):
        self.op1 = s;
    def mux_op2(self, s):
        self.op2 = s;
    def mux_condition(self, s):
        self.types = s
    def mux_left_op(self, s):
        self.left_op = s
    def mux_right_op(self, s):
        self.right_op = s
    def mux_to(self, s):
        self.to = s
    def mux_sfrom(self, s):
        self.sfrom.append(s)

class signal():
    def __init__(self):
        self.name = ''
        self.types = ''
        self.width = ''
        self.to = []
        self.sfrom = []
    def signal_name(self, s):
        self.name = s
    def signal_width(self, s):
        self.width = s
    def signal_type(self, s):
        self.types = s
    def signal_to(self, s):
        self.to.append(s)
    def signal_from(self, s):
        self.sfrom.append(s)

class constant():
    def __init__(self):
        self.name = ''
        self.types = ''
        self.width = ''
        self.to = []
        self.value = ''
    def constant_name(self, s):
        self.name = s
    def constant_width(self, s):
        self.width = s
    def constant_type(self, s):
        self.types = s
    def constant_to(self, s):
        self.to.append(s)
    def constant_value(self, s):
        self.value = s

class operator:
    def __init__(self):
        self.name = ''
        self.types = ''
        self.sfrom = []
        self.to = ''
    def operator_name(self, s):
        self.name = s
    def operator_type(self, s):
        self.types = s
    def operator_to(self, s):
        self.to = s
    def operator_from(self, s):
        self.sfrom.append(s)

port_instance = port()
mux_instance = mux()
signal_instance = signal()
constant_instance = constant()
operator_instance = operator()
mux_instance=mux()
def update(s, t):
    if s[0] == 's':
        signal_list[s[1]].signal_to(t)
    if s[0] == 'c':
        signal_list[s[1]].constant_to(t)
    if s[0] == 'p':
        port_list[s[1]].port_to(t)

def list_2_s(s):
    st = ''
    for element in s:
        if type(element) == type(operator_instance) :
            st = st + ' O' + str(element.name) + ', '
        else:
            if type(element)==type(mux_instance):
                st = st + ' M' + str(element.name)
            else:
                st = st + str(element) + ', '
    return st

def operator_check(s):
    for element in operator_array:
        if s.find(element) != -1:
            return operator_array.index(element)
    return -1

def condition_check(s):
    for element in condition_list:
        if s.find(element) != -1:
            return condition_list.index(element)
    return -1

def element_list_find(s):
    i = -1
    s_list = ['', i]
    for element in signal_list:
        if element.name == s:
            if type(signal_list[signal_list.index(element)]) == type(signal_instance):
                s_list[0] = 's'
                i = signal_list.index(element)
            else:
                s_list[0] = 'c'
                i = signal_list.index(element)
                continue
    if i == -1:
        for element in port_list:
            if element.name == s:
                i = port_list.index(element)
                s_list[0] = 'p'
                continue
    s_list[1] = i
    return s_list



def entity_check():
    global entity_find
    global port_status
    global entity_name
    if entity_find == 1 and port_status == 2:
        return
    if entity_find == 0:
        if 'entity' in e_array:
            entity_find = 1
            entity_name = e_array[e_array.index('entity') + 1]
            return
    if entity_find == 1 and port_status == 0:
        if 'port' in e_array:
            port_status = 1
            return
    if entity_find == 1 and port_status == 1:
        if 'end;' in e_array:
            port_status = 2
            return
        else:
            base = e_array.index(':')
            name = e_array[base - 1]
            direction = e_array[base + 1]
            types = e_array[base + 2]
            if types == 'STD_LOGIC;' or types == 'STD_LOGIC':
                width = '1'
            else:
                width = int(e_array[base + 3][1: ]) + 1
            s = port()
            s.port_name(name)
            s.port_direction(direction)
            s.port_type(types)
            s.port_width(width)
            port_list.append(s)
            return


def signal_check():
    global entity_find
    global port_status
    global signal_find
    if entity_find == 1 and port_status == 2:
        if signal_find == 0:
            if 'architecture' in e_array:
                signal_find = 1
                return
        if signal_find == 1:
            if 'signal' in e_array:
                base = e_array.index(':')
                name = e_array[base - 1]
                types = e_array[base + 1]
                if types == 'STD_LOGIC':
                    width = '1'
                else:
                    width = int(e_array[base + 2][1: ]) + 1
                    s = signal()
                    s.signal_name(name)
                    s.signal_type(types)
                    s.signal_width(width)
                    signal_list.append(s)
                    return
            if 'constant' in e_array:
                base = e_array.index(':')
                name = e_array[base - 1]
                types = e_array[base + 1]
                if types == 'STD_LOGIC' or types == 'BOOLEAN':
                    width = '1'
                else:
                    width = int(e_array[base + 2][1: ]) + 1
                    value = e_array[len(e_array) - 1]
                    value = value[: len(value) - 1]
                    s = constant()
                    s.constant_name(name)
                    s.constant_type(types)
                    s.constant_width(width)
                    s.constant_value(value)
                    signal_list.append(s)
                    return
            if 'begin' in e_array:
                signal_find = 2
                return



def process_check():
    global signal_find
    global process_find
    global process_valid
    if signal_find == 2:
        e_st = ''
        for element in e_array:
            e_st = e_st + element
        ic1 = e_st.find('ap_CS_fsm')
        ic2 = e_st.find('ap_NS_fsm')
        ic3 = e_st.find('ap_vld')
        if process_find == 0:
            if e_st.find('process') != -1 and e_st.find('end') == -1:
                process_find = 1
                if (ic1 == -1 and ic2 == -1 and ic3 == -1):
                    process_valid = 1
                else:
                    process_valid = 0
                return
        if process_find == 1 and process_valid == 1:
            if e_st.find('<=') != -1:
                base = e_array.index('<=')
                to = e_array[base - 1]
                sfrom = ''
                sfromp = ''
                if 'downto' in e_array:
                    mid = e_array.index('downto')
                    sfrom = e_array[mid - 1] + e_array[mid] + e_array[mid + 1].replace(';', '')
                    sfromp = e_array[mid - 1][: e_array[mid - 1].index('(')]
                else:
                    sfromp = sfrom = e_array[base + 1].replace(';', '')
                to_info = element_list_find(to)
                from_info = element_list_find(sfromp)
                if to_info[0] == 's':
                    signal_list[to_info[1]].signal_from(sfrom)
                if to_info[0] == 'c':
                    signal_list[to_info[1]].constant_from(sfrom)
                if to_info[0] == 'p':
                    port_list[to_info[1]].port_from(sfrom)
                    update(from_info, to)
                    return
        if 'end' in e_array and 'process;' in e_array:
            process_find = 0
            process_valid = 0
            return




def statement_check():
    global operator_count
    global signal_find
    global process_find
    global process_valid
    if signal_find == 2:
        if process_find == 0 and process_valid == 0 and '<=' in e_array:
            base = e_array.index('<=')
            to = e_array[base - 1]
            e_st = ''
            count = base + 1
            while(count < len(e_array)):
                e_st = e_st + e_array[count]
                count = count + 1
            e_st = e_st.replace(';', '')
            e_st = e_st.replace('std_logic_vector', '')
            e_st = e_st.replace('unsigned', '')
            e_st = e_st.replace('signed', '')
            if e_st.find('resize') != -1:
                pos0 = e_st.index('resize')
                e_st_temp = e_st[pos0: ]
                pos00 = e_st_temp.index('(')
                pos1 = e_st_temp.index(',')
                e_st_tt = e_st_temp[pos1: ]
                pos2 = e_st_tt.index(')')
                e_st = e_st[ :pos0]+e_st_temp[pos00: pos1] + e_st_tt[pos2: ]
            if e_st.find('&') != -1:
                print(e_st)
                pos0 = e_st.index('&')
                print(pos0)
                decre = 0
                while(e_st[pos0 - decre] != '('):
                    print(e_st[pos0-decre])
                    decre = decre + 1
                e_st = e_st[: pos0 - decre] + e_st[pos0 + 1: ]
            if 'downto' not in e_st:
                e_st = e_st.replace('(', '')
                e_st = e_st.replace(')', '')
            if e_st.find('when') != -1:
                for element in e_array:
                    e_array[e_array.index(element)]=element.replace(';','')
                pos0 = e_array.index('when')
                pos1 = e_array.index('else')
                arg1 = e_array[pos0 - 1]
                arg2 = e_array[pos1 + 1]
                p0 = e_st.index('when')
                p1 = e_st.index('else')
                cond = e_st[p0 + 4: p1]
                c_pos = condition_check(cond)
                c_op = condition_list[c_pos]
                s = mux()
                s.mux_name(operator_count)
                operator_count = operator_count + 1
                s.mux_op1(arg1)
                s.mux_op2(arg2)
                arg1_info = element_list_find(arg1)
                arg2_info = element_list_find(arg2)
                update(arg1_info, s)
                update(arg2_info, s)
                s.mux_condition(c_op)
                left = cond[: cond.index(c_op)]
                right = cond[cond.index(c_op) + 1: ]
                s.mux_left_op(left)
                s.mux_right_op(right)
                mux_list.append(s)
                left_info = element_list_find(left)
                right_info = element_list_find(right)
                if left_info[0] != '':
                    update(left_info, s)
                if right_info[0] != '':
                    update(right_info, s)
                to_info = element_list_find(to)
                print(to)
                print(to_info)
                if to_info[0] == 's':
                    signal_list[to_info[1]].signal_from(s)
                if to_info[0] == 'p':
                    port_list[to_info[1]].port_from(s)
                print('\n')
                return

            if operator_check(e_st) != -1:
                op = operator_check(e_st)
                pos = e_st.index(operator_array[op])
                to_info = element_list_find(to)
                left_info = element_list_find(e_st[: pos])
                right_info = element_list_find(e_st[pos + 1: ])
                s = operator()
                s.operator_name(operator_count)
                operator_count = operator_count + 1
                s.operator_type(operator_array[op])
                s.operator_to(to)
                if left_info[0] == 'p':
                    left_op = port_list[left_info[1]].name
                else:
                    left_op = signal_list[left_info[1]].name
                if right_info[0] == 'p':
                    right_op = port_list[right_info[1]].name
                else:
                    right_op = signal_list[right_info[1]].name
                s.operator_from(left_op)
                s.operator_from(right_op)
                operator_list.append(s)
                update(left_info, s)
                update(right_info, s)
                if to_info[0] == 's':
                    signal_list[to_info[1]].signal_from(s)
                if to_info[0] == 'p':
                    port_list[to_info[1]].port_from(s)
                return
            else:
                to_info = element_list_find(to)
                if to_info[0] == 's':
                    signal_list[to_info[1]].signal_from(e_st)
                if to_info[0] == 'p':
                    port_list[to_info[1]].port_from(e_st)
                e_st_info = element_list_find(e_st)
                update(e_st_info, to)
                return




def end_check():
    if 'end' in e_array and 'behav;' in e_array:
        entity_find = 0
        port_status = 0
        signal_find = 0
        process_find = 0
        process_valid = 0
        operator_count = 0


for line in fin.readlines():
    if line_extend == 0:
        e_array = []
    line = line.replace('\n', '')
    if '--' in line:
        continue
    for element in line.split(" "):
        e_array.append(element)

    while '' in e_array:
        for element in e_array:
            if element == '':
                del e_array[e_array.index(element)]

    if len(e_array) == 0:
        continue

    last = e_array[len(e_array) - 1]
    if last.find(';') == -1 and (last.find('<=') != -1 or last.find('else') != -1):
        line_extend = 1
        continue
    else:
        line_extend = 0
    print(e_array)
    entity_check()
    signal_check()
    process_check()
    statement_check()
    end_check()

fout.write('ENTITY NAME: ' + entity_name + '\n')

for e1 in port_list:
    fout.write("PORT " + e1.name + " {")
    fout.write("    DIRECTION: " + e1.direction)
    fout.write("    WIDTH: " + str(e1.width))
    fout.write("    TO: " + list_2_s(e1.to))
    fout.write("    FROM: " + list_2_s(e1.sfrom) + " }")
    fout.write("\n")
    fout.write('\n')

for e2 in signal_list:
    if type(e2) == signal:
        fout.write("SIGNAL " + e2.name + " {")
        fout.write("    WIDTH: " + str(e2.width))
        fout.write("    TO: " + list_2_s(e2.to))
        fout.write("    FROM: " + list_2_s(e2.sfrom) + " }")
        fout.write("\n")
    if type(e2) == constant:
        fout.write("CONSTANT " + e2.name + " {")
        fout.write("    WIDTH: " + str(e2.width))
        fout.write("    VALUE: " + str(e2.value))
        fout.write("    TO: " + list_2_s(e2.to) + " }")
        fout.write('\n')

for e4 in operator_list:
    fout.write('OPERATOR ' + str(e4.name) + ' {')
    fout.write('    TYPE: ' + str(e4.types))
    fout.write('    TO: ' + (e4.to))
    fout.write('    FROM: ' + list_2_s(e4.sfrom) + ' }')
    fout.write('\n')

for e5 in mux_list:
    fout.write('MUX '+ str(e5.name) + ' {')
    fout.write('    TYPE: '+str(e5.types))
    fout.write('    ARGUMENTS: '+str(e5.op1)+' '+str(e5.op2))
    fout.write('    OPERANDS: '+str(e5.left_op)+' '+str(e5.right_op))
    fout.write('\n')
