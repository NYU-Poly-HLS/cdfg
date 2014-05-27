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
operator_array = ['+', '-', '*', '/']
operator_list = []
mux_list = []
condition_list = ['=', '>', '<']
line_extend = 0
function_list = ['to_integer','sihft_left',",",'resize','signed','unsigned','+','-','*','&','(',')']
function_name_list=['to_integer','sll',",",'resize','signed','unsigned','add','sub','mul','&','(',')']
priority_list = [4,4,4,4,3,3,1,1,2,2,9,0]
parameter_find = 0
temp_count=0

class bit():
    def __init__(self):
        self.pos=''
        self.to=['',0]
        self.sfrom=['',0]
    def bit_place(self,s):
        self.pos=s
    def bit_to(self,name,pos):
        self.to[0]=name
        self.to[1]=pos
    def bit_from(self,name,pos):
        self.sfrom[0]=name
        self.sfrom[1]=pos

class port():
    def __init__(self):
        self.data=[]
        self.name = ''
        self.types = ''
        self.width = 0
        self.direction = ''
        self.to = []
        self.sfrom = []
    def port_name(self, s):
        self.name = s
    def port_direction(self, s):
        self.direction = s
    def port_width(self, s):
        self.width = s
        i=0
        while i < self.width:
            b=bit()
            b.bit_place(i)
            self.data.append(b);
            i=i+1
    def port_type(self, s):
        self.types = s
    def port_to_update(self):
        for bit in self.data:
            s=bit.to[0]
            if s not in self.to :
#                print('Port Update To')
                self.to.append(s)
    def port_from_update(self):
        for bit in self.data:
            s=bit.sfrom[0]
            if s not in self.sfrom:
#                print('Port Update From')
                self.sfrom.append(s)
    def port_to(self,s):
        self.to.append(s)
    def port_from(self,s):
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
        self.data=[]
        self.name = ''
        self.types = ''
        self.width = 0
        self.to = []
        self.sfrom = []
    def signal_name(self, s):
        self.name = s
    def signal_width(self, s):
        self.width = s
        i=0
        while i < self.width:
            b=bit()
            b.bit_place(i)
            self.data.append(b);
            i=i+1
    def signal_type(self, s):
        self.types = s
    def signal_to_update(self):
  #      print("!")
        for bit in self.data:
            s=bit.to[0]
            if s not in self.to :
                self.to.append(s)
#                print("Signal Update To")
    def signal_from_update(self):
        for bit in self.data:
            s=bit.sfrom[0]
            if s not in self.sfrom:
                self.sfrom.append(s)
#                print('Signal Update From')
    def signal_to(self,s):
        self.to.append(s)
    def signal_from(self,s):
        self.sfrom.append(s)


class constant():
    def __init__(self):
        self.data=[]
        self.name = ''
        self.types = ''
        self.width = 0
        self.to = []
        self.value=''
    def constant_name(self, s):
        self.name = s
    def constant_width(self, s):
        self.width = s
        i=0
        while i < self.width:
            b=bit()
            b.bit_place(i)
            self.data.append(b);
            i=i+1
    def constant_type(self, s):
        self.types = s
    def constant_to_update(self):
        for bit in self.data:
#            print("!!!!!!!")
            s=bit.to[0]
            if s not in self.to :
                self.to.append(s)
#                print('Constant Update To')
    def constant_to(self,s):
        self.to.append(s)
    def constant_value(self,s):
        self.value=s

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


class operator:
    def __init__(self):
        self.name = ''
        self.sign = ''
        self.types = ''
        self.sfrom = []
        self.to = ''
    def operator_name(self, s):
        self.name = s
    def operator_sign(self,s):
        self.sign = s
    def operator_type(self, s):
        self.types = s
    def operator_to(self, s):
        self.to = s
    def operator_from(self, s):
        self.sfrom.append(s)

port_instance=port()
signal_instance=signal()
constant_instance=constant()
mux_instance = mux()
operator_instance = operator()
FROM=1
TO=0

def update(s,mode):
#    print(s)
    if type(s)==type(port_instance):
        if mode==0:
            s.port_to_update()
        if mode==1:
            s.port_from_update()
        return
    if type(s)==type(signal_instance):
        if mode==0:
            s.signal_to_update()
        if mode==1:
            s.signal_from_update()
        return
    if type(s)==type(constant_instance):
#        print('Constant Find!')
        if mode==0:
            s.constant_to_update();
        if mode==1:
            print("CONSTANT NO FROM!\n")
        return


def assign(s1,s2,mode,p1,p2):
#    print('!')
#    print(s1.name)
#    print(s2.name)
#    print(str(mode))
    if mode==0:
        if len(s1.data)!=len(s2.data):
            print(s1.name)
            print(s2.name)
            print("MISMTACH!\n")
        for bit1 in s1.data:
            index=s1.data.index(bit1)
            bit1.sfrom[0]=s2.name
            bit1.sfrom[1]=index
            s2.data[index].to[0]=s1.name
            s2.data[index].to[1]=index
        update(s1,FROM)
        update(s2,TO)
        return
    if mode==1:
        s1.data[p1].sfrom[0]=s2.name
        s1.data[p1].sfrom[1]=p2
        s2.data[p2].to[0]=s1.name
        s2.data[p2].to[1]=p1
        update(s1,FROM)
        update(s2,TO)
        return
    if mode==2:
        s1.data[p1].sfrom[0]=s2
        s1.data[p1].sfrom[1]=-1
        return

def operator_check(s):
    for element in operator_array:
        if s.find(element) != -1:
            return operator_array.index(element)
    return -1
SIGNED=1
UNSIGNED=0




def node_find(s):
    for element in signal_list:
        if element.name==s:
            return element

    for element in port_list:
        if element.name==s:
            return element

def simple_assignment(l):
#    print('simple_assignment')
#    print(l)
    base=l.index('<=')
    left=l[base-1]
    right=l[base+1]
    right=right.replace(';','')
    left_name=''
    right_name=''
    lup_range=-1
    llow_range=-1
    lpos=-1
    rup_range=-1
    rlow_range=-1
    rpos=-1
    if left.find('(')!=-1:
        left_name=left[:left.find('(')]
        if left.find('downto')!=-1:
            pos_temp=l.index('downto')+1
            lup_range=int(left[left.find('(')+1:])
            llow_range=int(l[pos_temp][:len(l[pos_temp])-2])
        else:
            pos_temp=left.index(')')
            lpos=int(left[left.index('(')+1:left.index(')')])
    else:
        left_name=left

    if right.find('(')!=-1:
        right_name=right[:right.find('(')]
        if right.find('downto')!=-1:
            pos_temp=l.index('downto')+1
            rup_range=int(right[right.find('(')+1:])
            rlow_range=int(l[pos_temp][:len(l[pos_temp])-2])
        else:
            pos_temp=right.index(')')
            rpos=int(right[right.index('(')+1:right.index(')')])
    else:
        if '"' in right:
            rpos=-2
            st=right[right.index('"'):len(right)-3]
        else:
            right_name=right

    if lpos==-1 and lup_range==-1:
        if rpos==-1 and rup_range==-1:
  #          print(left_name)
  #          print(right_name)
            assign(node_find(left_name),node_find(right_name),0,0,0)
            return
        if rpos!=-1 and rpos!=-2:
            assign(node_find(left_name),node_find(right_name),1,0,rpos)
            return
        if rup_range!=-1:
            i=rlow_range
            while(i<=rup_range):
                assign(node_find(left_name),node_find(right_name),1,i-rlow_range,i)
                i=i+1
            return
        if rpos==-2:
            i=0
            while(i<=(len(st)-1)):
                assign(node_find(left_name),int(st[i]),2,len(st)-1-i,0)
                i=i+1
            return

    if lpos!=-1:
        if rpos==-1 and rup_range==-1:
            assign(node_find(left_name),node_find(right_name),0,lpos,0)
            return
        if rpos!=-1 and rpos!=-2:
            assign(node_find(left_name),node_find(right_name),1,lpos,rpos)
        if rpos==-2:
            assign(node_find(left_name),int(st),2,0,0)

    if lup_range!=-1:
        if rpos==-1 and rup_range==-1:
            i=llow_range
            while(i<=lup_range):
                assign(node_find(left_name),node_find(right_name),1,i,i-llow_range)
                i=i+1
            return
        if rup_range!=-1:
            i=llow_range
            j=rlow_range
            while(i<=lup_range):
                assign(node_find(left_name),node_find(right_name),1,i,j)
                i=i+1
                j=j+1
            return
        if rpos==-2:
            i=llow_range
            while(i<=lup_range):
                assign(node_find(left_range),int(st[i-llow_range]),2,i,0)
                i=i+1
            return

def function_check(s):
    global function_list
    global parameter_find
    if s=='to_integer':
        parameter_find=3
        return
    if s==',':
        parameter_find=1
        return
    if s=='downto':
        parameter_find=2
        return
    if s in function_list:
        return 1
    else:
        return 0

def complex_assignment(l):
 #   print(l)
    global parameter_find
    global operator_count
    global temp_count
    global signal_list
    global port_list
    output_list=[]
    op_list=[]
    base=l.index('<=')
    left=l[base-1]
    st=''
    for element in l[base+1:]:
        st=st+element
    st=st.replace('std_logic_vector','')
    st=st.replace(';','')
    word=''
    progress=0
#    print('complex_assignment')
    while(progress<=len(st)-1):
        if(len(word)==0):
            word=word+st[progress]
            progress=progress+1
#        print(word)
        func_state=function_check(word)
        element_state=element_check(word)[1]
#        print(str(func_state)+' '+str(element_state)+' '+str(parameter_find)+' '+word[len(word)-1])
        if parameter_find==1 and word[len(word)-1]==')':
#            print("!!!!")
#            print(word)
#            print(len(word))
            output_list.append(word[1:len(word)-1])
            word=word[len(word)-1]
            func_state=function_check(word)
            element_state=element_check(word)[1]
            parameter_find=0
        if parameter_find==2 and word[len(word)-1]==')':
            output_list[len(output_list)]=output_list[len(output_list)]+'('+word
            list_pop(op_list)
            parameter_find=0
            continue
        if parameter_find==3:
            word=''
            parameter_find=0
            continue
        if element_state!=-1 and (st[progress]==')' or word[len(word)-1]=="'"):
            output_list.append(word)
            word=''
            continue
        if func_state==1:
#            print('HERE')
#           print(op_list)
            current_order=function_list.index(word)
            current_priority=priority_list[current_order]
            if(len(op_list)==0):
                op_list.append(word)
                word=''
                continue
            op_last=op_list[len(op_list)-1]
            op_last_priority=priority_list[function_list.index(op_last)]
#            print(str(current_priority)+' '+str(op_last_priority))
            if current_priority>=op_last_priority:
                op_list.append(word)
                word=''
                continue
            else:
                exe=0
                while(current_priority<op_last_priority):
                    if op_list[len(op_list)-1]=='(' and word==')':
                        list_pop(op_list)
                        exe=0
                        break
                    else:
                        if(op_list[len(op_list)-1]!='('):
                            output_list.append(list_pop(op_list))
                            op_last=len(op_list)-1
                            op_last_priority=priority_list[function_list.index(op_list[op_last])]
                            exe=1
                        else:
                            exe=1
                            break
             #   print('!!!')
                if exe==1:
                    op_list.append(word)
                word = ''
                continue
        else:
#            print("IN")
            word=word+st[progress]
            progress=progress+1
            continue
    while(len(op_list)!=0):
        if op_list[len(op_list)-1]=='(' or op_list[len(op_list)-1]==')':
            list_pop(op_list)
        else:
            output_list.append(list_pop(op_list))
    for element in output_list:
        num=output_list.index(element)
        if element==',':
            del output_list[num]

    buffer_list=[]
  #  print(output_list)
    for element in output_list:
#        print('#B ')
#        print(buffer_list)
#        print(element)
#        print('\n\n')
        node=[element,'unsigned']
        if element=='signed':
            buffer_list[len(buffer_list)-1][1]='signed'
            continue
        if element=='unsigned':
            buffer_list[len(buffer_list)-1][1]='unsigned'
            continue
        if element=='+' or element=='-' or element=='*' or element=='resize' or element=='shift_left' or element=='&':
            sign1=buffer_list[len(buffer_list)-1][1]
            name1=buffer_list[len(buffer_list)-1][0]
            width1=0
            if '"' in name1:
 #               print(name1)
                width1=element_check(name1)[0]
            else:
 #               print(name1)
                if '(' in name1:
                    start=name1.index('(')
                    mid=name1.index('downto')
                    end=name1.index(')')
                    head=name1[start+1:mid]
                    tail=name1[mid+6:end]
                    lower_bound=int(tail)
                    upper_bound=0
                    if '-' in head:
                        pos=head.index('-')
                        f1=int(head[:pos])
                        f2=int(head[pos+1:])
                        upper_bound=f1-f2
                    else:
                        upper_bound=int(head)
                    width1=upper_bound-lower_bound
                else:
                    status=element_check(name1)
                    if status[0]=='s' or status[0]=='c':
                        width1=signal_list[status[1]].width
                    else:
                        if status[0]=='p':
                            width1=port_list[status[1]].width
                        else:
                            width1=int(name1)
            sign2=buffer_list[len(buffer_list)-2][1]
            name2=buffer_list[len(buffer_list)-2][0]
            withd2=0
            if ('"' in name2 or "'" in name2):
                width2=element_check(name2)[0]
    #            print(width2)
            else:
                if '(' in name2:
                    start=name2.index('(')
                    mid=name2.index('downto')
                    end=name2.index(')')
                    head=name2[start+1:mid]
                    tail=name2[mid+6:end]
                    lower_bound=int(tail)
                    upper_bound=0
                    if '-' in head:
                        pos=head.index('-')
                        f1=int(head[:pos])
                        f2=int(head[pos+1:])
                        upper_bound=f1-f2
                    else:
                        upper_bound=int(head)
                        width2=upper_bound-lower_bound
                else:
                    status=element_check(name2)
                    if status[0]=='s' or status[0]=='c':
                        width2=signal_list[status[1]].width
                    else:
                        if status[0]=='p':
                            width2=port_list[status[1]].width
                        else:
                            width2=int(name2)
   #         print(name1+' '+name2)
   #         print(str(width1)+' '+str(width2))
            state1=element_check(name1)
            state2=element_check(name2)
            if sign1=='unsigned' and sign2=='unsigned':
                sign = 'unsigned'
            else:
                sign = 'signed'
            op=operator()
            op.operator_name('Op'+str(operator_count))
            operator_count=operator_count+1
            op.operator_sign(sign)
            if element=='&':
                op.operator_type('assign')
            else:
                op.operator_type(element)
            op.operator_from(name1)
            op.operator_from(name2)
            operand1=element_list_find(name1)
            operand2=element_list_find(name2)
            if operand1[1]!=-1:
                if operand1[0]=='s':
                    signal_list[operand1[1]].signal_to(op.name)
                if operand1[0]=='p':
                    port_list[operand1[1]].port_to(op.name)
                if operand1[0]=='c':
                    signal_list[operand1[1]].constant_to(op.name)
            if operand2[1]!=-1:
                if operand2[0]=='s':
                    signal_list[operand2[1]].signal_to(op.name)
                if operand2[0]=='p':
                    port_list[operand2[1]].port_to(op.name)
                if operand2[0]=='c':
                    signal_list[operand2[1]].constant_to(op.name)


            si=signal()
            si.signal_name('stemp'+str(temp_count))
            op.operator_to(si.name)
            temp_count=temp_count+1
            if element=='resize' or element=='shift_left':
           #     print(name1)
           #     print(str(width1))
           #     print(name2)
           #     print(str(width2))
                si.signal_width(width2)
            else:
                if element=='&':
  #                  print(str(width1))
  #                  print(str(width2))
                    si.signal_width(width1+width2)
                else:
                    si.signal_width(max(width1,width2))
            si.signal_from(op)
            signal_list.append(si)
            operator_list.append(op)
#            print(buffer_list)
            list_pop(buffer_list)
            list_pop(buffer_list)
            node=[si.name,'unsigned']
            buffer_list.append(node)
            continue
        else:
            buffer_list.append(node)
#    print(buffer_list)
    line=[left,'<=',buffer_list[0][0]]
    simple_assignment(line)
#    s_name=(list_pop(buffer_list)[0])
#    s_status=element_list_find(s_name)

#    print(signal_list[len(signal_list)-1].name)

def list_pop(s):
    last=s[len(s)-1]
    del s[len(s)-1]
    return last



def element_check(s):
    test_pos=s.find("'")
    slist=['',0]
 #   print(s[test_pos+1:].find("'")!=-1 and test_pos!=-1)
    if s[test_pos+1:].find("'")!=-1 and test_pos!=-1:
        slist=[s[test_pos+1:].find("'"),1]
 #       print(slist)
        return slist
    else:
        slist=element_list_find(s)
        return slist

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

#def update(s, t):
#    if s[0] == 's':
#        signal_list[s[1]].signal_to(t)
#    if s[0] == 'c':
#        signal_list[s[1]].constant_to(t)
#    if s[0] == 'p':
#        port_list[s[1]].port_to(t)

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
                width = 1
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
#                    print(name)
                    signal_list.append(s)
                    return
            if 'constant' in e_array:
                base = e_array.index(':')
                name = e_array[base - 1]
                types = e_array[base + 1]

                if types == 'STD_LOGIC' or types == 'BOOLEAN':
                    width = 1
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
#                print(name)
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
                simple_assignment(e_array)
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
  #              print(to)
  #              print(to_info)
                if to_info[0] == 's':
                    signal_list[to_info[1]].signal_from(s)
                if to_info[0] == 'p':
                    port_list[to_info[1]].port_from(s)
  #              print('\n')
                return

            if operator_check(e_st) != -1:
                complex_assignment(e_array)
            else:
                simple_assignment(e_array)

def end_check():
    if 'end' in e_array and 'behav;' in e_array:
        entity_find = 0
        port_status = 0
        signal_find = 0
        process_find = 0
        process_valid = 0
        operator_count = 0

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
#    print(e_array)
    entity_check()
    signal_check()
    process_check()
    statement_check()
    end_check()

#fout.write('ENTITY NAME: ' + entity_name + '\n')

for e1 in port_list:
#    fout.write("PORT " + e1.name + " {")
#    fout.write("    DIRECTION: " + e1.direction)
#    fout.write("    WIDTH: " + str(e1.width))
#    fout.write("    TO: " + list_2_s(e1.to))
#    fout.write("    FROM: " + list_2_s(e1.sfrom) + " }")
#    fout.write("\n")
#    fout.write('\n')
    if e1.name=='ap_clk' or e1.name=='ap_rst' or e1.name=='ap_vld':
        continue
    if e1.direction=='IN':
        fout.write('input('+e1.name+') {'+'\n')
        fout.write('    bandwidth '+str(e1.width)+';\n')
        fout.write('    signed 0;\n')
        fout.write('}')
    else:
        fout.write('output('+e1.name+') {'+'\n')
        fout.write('    bandwidth '+str(e1.width)+';\n')
        fout.write('    signed 0;\n')
        fout.write('}')
    fout.write('\n')

for e2 in signal_list:
    if type(e2) == signal:
        fout.write('variable('+e2.name+') {'+'\n')
        if e2.name.find('reg')!=-1:
            n=e2.sfrom[0]
            fout.write('    aging '+n+';\n')
        fout.write('    bandwidth '+str(e2.width)+';\n')
        fout.write('    signed 0;\n')
        fout.write('    value 0;\n')
        fout.write('}')
    if type(e2) == constant:
        fout.write('constants('+e2.name+') {'+'\n')
        fout.write('    bandwidth '+str(e2.width)+';\n')
        fout.write('    signed 0;\n')
        fout.write('    value '+e2.value[1:len(e2.value)-1]+';\n')
        fout.write('}')
    fout.write('\n')


for e4 in operator_list:
#    fout.write('OPERATOR ' + str(e4.name) + ' {')
#    fout.write('    TYPE: ' + str(e4.types))
#    fout.write('    SIGN: ' + str(e4.sign))
#    fout.write('    TO: ' + (e4.to))
#    fout.write('    FROM: ' + list_2_s(e4.sfrom) + ' }')
#    fout.write('\n')
    print(e4.types)
    print(e4.sfrom)
    fout.write('operation'+'(op'+str(operator_list.index(e4))+') {'+'\n')
    fout.write('    function '+ function_name_list[function_list.index(e4.types)]+';\n')
    fout.write('    read '+e4.sfrom[0]+','+e4.sfrom[1]+';\n')
    fout.write('    write '+e4.to+';\n')
    fout.write('}')
    fout.write('\n')

for e5 in mux_list:
    fout.write('MUX '+ str(e5.name) + ' {')
    fout.write('    TYPE: '+str(e5.types))
    fout.write('    ARGUMENTS: '+str(e5.op1)+' '+str(e5.op2))
    fout.write('    OPERANDS: '+str(e5.left_op)+' '+str(e5.right_op))
    fout.write('\n')
