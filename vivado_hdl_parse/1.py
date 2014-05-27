import sys

if len(sys.argv)!=2:
    print("Usage: 1.py <filename>");
    sys.exit;
fin = open(sys.argv[1],"r")

# flags: global variables
entity_found=0;
architecture_begin=0;
ports_begin=0;
ports_done=0;
const_found=0;
temp=0;
signal_found=0
process_state=0
tt=[]

class Operator:
    name=0;
    input_list=[]
    output_list=[]
    def set_name(self,name_in):
        self.name=name_in
    def input_add(self,in_list):
        self.input_list.append(in_list)
    def output_add(self,out_list):
        self.output_list.append(out_list)
#    def __init__(self):

class Input:
    name=0
    node_out=0
    def seto(self,f_in):
        self.node_out=f_in
    def set_name(self,n_in):
        self.name=n_in
#    def __init__(self):

class Output:
    name=0
    node_in=0
    def seti(self,b_in):
        self.node_in=b_in
    def set_name(self,n_in):
        self.name=n_in

#    def __init__(self):

class Signal:
    name=0
    node_out=0
    node_in=0
    def seto(self,f_in):
            self.node_out=f_in
    def seti(self,b_in):
           self.node_in=b_in
    def set_name(self,n_in):
            self.name=n_in
#    def __init__(self):

class Const:
    name=0
    value=0
    def set_name(self,n_in):
        self.name=n_in
    def set_value(self,v_in):
        self.value=v_in
#    def __init__(self):



#Const array
const_array=[]
#Output array
output_array=[]
#Input array
input_array=[]
#Signal array
signal_array=[]

#define functions
# identify entity
def entity(s):
    global entity_found
    if(entity_found==0):
        if s=='entity':
            print("ENTITY IS ")
            entity_found=1
    else:
        if(entity_found==1):
            print(s)
            entity_found=2

#identify IO
def IO(s):
    global ports_begin
    global ports_done
    global word_buf1
    global line_temp
    global line_done
    global input_array
    global output_array
    global inflag,outflag
    global t
    next_word=0
    if ports_begin==0 and ports_done==0:
        if s=='port':
            ports_begin=1
            print ("PORTS ARE")
    else:
        if (line_done==0 and ports_begin==1 and ports_done==0):
            for inv in line_temp.split(" "):
                if inv=='NI':
                    inflag=1;
                if inv=='TUO':
                    outflag=1;
                if inv ==':':
                    next_word=1
                else:
                    if next_word==1:
                        print(inv[::-1])
                        if(inflag==1):
                            t1=Input()
                            t1.set_name(inv[::-1])
                            input_array.append(t1)
                        else:
                            t1=Output()
                            t1.set_name(inv[::-1])
                            output_array.append(t1)
                        line_done=1
                if inv =="\n;)":
                    ports_begin = 0
                    ports_done=1
                    line_done=1

#identify constants
def consts(s):
    const_num=Const()
    global const_found
    if(s=='constant'):
        const_found=1;
     #   print('CONST FOUND')
    else:
        if(const_found==1):
            print(s)
            const_found=2
            const_num.set_name(s)
            const_found=2
        else:
            if(const_found==2):
                inv_str=line_temp.split(" ")
                inv=inv_str[0]
                inv_value=str(inv[3:len(inv)-1])
                inv_value=inv_value[::-1]
                inv_value=int(inv_value,2)
             #   print(inv_value)
                const_num.set_value(inv_value)
                const_found=3

#identify signal
def signal(s):
    global signal_found
    if s=='signal':
        signal_found=1;
    else:
        if signal_found==1:
            signal_found=2
            t=Signal()
            t.set_name(s)
            signal_array.append(t)


#statements handler
def assign(s):
    nesting=0
    if ('<=') in s:
        print("Assign!")
        i=s.index('<=')
        for right in s[i+1:]:
            if right.find('(')!=-1:
                nesting++
            if right.find('\n')!=-1:
                right=right[:len(right)-2]
                print (right)




#process handler


for line in fin.readlines():
    line_temp=line[::-1]
    line_done=0
    for temp in line.split(" "):
        if architecture_begin==0:
            entity(temp)
            IO(temp)
            consts(temp)
            signal(temp)
            if(temp=='begin\n'):
                architecture_begin=1
        tt.append(temp)
    assign(tt)
    if architecture_begin==1:
        print (tt)

    tt=[]

           #  if(architecture_begin==1)
           # print(temp)
