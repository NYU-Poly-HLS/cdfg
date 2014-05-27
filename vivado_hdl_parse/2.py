import sys
if len(sys.argv)!=2:
    print("Usage: 2.py <filename>");
    sys.exit;
fin = open(sys.argv[1],"r")
#fin = open('dir.vhd','r')
out = sys.argv[1]
filename = out[:len(out)-4] + ".txt"
fout = open (filename, "w")

#Constants
entity_found=0;
port_begin=0;
port_done=0;
process_begin=0
process_done=0
architecture_begin=0;
signal_done=0;
element_array=[]
port_array=[]
constant_array=[]
signal_array=[]
operator_array=[]
entity_name=0;
operator_count=0
op_type=''


class port():
    direction=0
    name=0
    width=0
    to=0
    sfrom=0
    def port_name(self,s):
        self.name=s
    def port_direction(self,s):
        self.direction=s
    def port_width(self,s):
        self.width=s
    def port_to(self,s):
        self.to=s
    def port_sfrom(self,s):
        self.sfrom=s

#    def __init__(self):

class constant:
    name=0
    width=0
    value=0
    to=0
    def constant_name(self,s):
        self.name=s
    def constant_width(self,s):
        self.width=s
    def constant_value(self,s):
        self.value=s
    def constant_to(self,s):
        self.to=s

#    def __init__(self):

class signal:
    name=0
    width=0
    sfrom=0
    to=''
    def signal_name(self,s):
        self.name=s
    def signal_width(self,s):
        self.width=s
    def signal_sfrom(self,s):
        self.sfrom=s
    def signal_to(self,s):
        self.to=s

#    def __init__(self):

def array_update(name,op_name,mode):
    sp=array_index(port_array,name)
    sc=array_index(constant_array,name)
    ss=array_index(signal_array,name)
    width=0
    if mode==0:
        if sp!=-1:
            port_array[sp].port_to(op_name)
            width=port_array[sp].width
        if sc!=-1:
            constant_array[sc].constant_to(op_name)
            width=constant_array[sc].width
        if ss!=-1:
            signal_array[ss].signal_to(op_name)
            width=signal_array[ss].width
    else:
        if sp!=-1:
            port_array[sp].port_sfrom(op_name)
            width=port_array[sp].width
        if ss!=-1:
            signal_array[ss].signal_sfrom(op_name)
            width=signal_array[ss].width
    return width


def max(a,b):
    if a>=b:
        return a
    else:
        return b



def array_index_all(n):
    pa=array_index(port_array,n)
    ca=array_index(constant_array,n)
    sa=array_index(signal_array,n)
    pl=['parr',str(pa)]
    cl=['carr',str(ca)]
    sl=['sarr',str(sa)]
    if pa!=-1:
        return pl
    if ca!=-1:
        return cl
    if sa!=-1:
        return sl


def array_index(q,n):
    i=0
    name_found=0
    for element in q:
        if element.name==n:
            name_found=1
            break
        else:
            i=i+1
    if name_found==1:
        return i
    else:
        return -1

def remove(s,q):
    if q in s:
        s=s.replace(q,'')
    return s

class operator:
    name=0
    width=0
    type=0
    sfrom0=0
    sfrom1=0
    to=0
    def operator_name(self,s):
        self.name=s
    def operator_type(self,s):
        if s=="+":
            self.type="adder"
        if s=="-":
            self.type="subtractor"
        if s=="*":
            self.type="multiplier"
    def operator_sfrom0(self,s):
        self.sfrom0=s
    def operator_sfrom1(self,s):
        self.sfrom1=s
    def operator_to(self,s):
        self.to=s
    def operator_width(self,s):
        self.width=s
 #   def __init__(self):


for line in fin.readlines():
    element_array=[]
    line=line.replace('\n','')
    for word in line.split(" "):
        element_array.append(word)
    if 'end' in element_array and 'behav;' in element_array:
        break
    if entity_found==0:
        if "entity" in element_array:
            entity_name=element_array[element_array.index("entity")+1]
            entity_found=1

    if port_begin==0:
        if "port" in element_array:
            port_begin=1
    if port_begin==1 and port_done==0:
        if ":" in element_array:
            base=element_array.index(":")
            name=element_array[base-1]
            direction=element_array[base+1]
            if element_array[base+2]=="STD_LOGIC;" or element_array[base+2]=="STD_LOGIC":
                width=1
            else:
                width=element_array[base+3]
                width=(width[1:])
                width=int(width,10)+1
            p=port()
            p.port_name(name)
            p.port_direction(direction)
            p.port_width(width)
            port_array.append(p)
        if "end;" in element_array:
            port_done=1

    if architecture_begin==0:
        if "architecture" in element_array:
            architecture_begin=1
    if architecture_begin==1 and signal_done==0:
        if "constant" in element_array:
            base=element_array.index(":")
            name=element_array[base-1]
            if element_array[base+1]=="STD_LOGIC":
                width=1
                value=element_array[base+3]
                value=value[1:2]
                #constant value are numbers or strings? string for now
            else:
                width=element_array[base+2]
                width=width[1:]
                if width=='0':
                    width=0
                else:
                    width= int(width,10)+1
                value=element_array[base+6]
                value=value[1:len(value)-2]
            cc=constant()
            cc.constant_name(name)
            cc.constant_width(width)
            cc.constant_value(value)
            constant_array.append(cc)
        if "signal" in element_array:
            base=element_array.index(":")
            name=element_array[base-1]
            if element_array[base+1]=="STD_LOGIC":
                width=1
                #constant value are numbers or strings? string for now
            else:
                width=element_array[base+2]
                width=width[1:]
                if width=='0':
                    width=0
                else:
                    width=(int(width,10)+1)
            ss=signal()
            ss.signal_name(name)
            ss.signal_width(width)
            signal_array.append(ss)
        if "begin" in element_array:
            signal_done=1

    if signal_done==1:
        if "--" in element_array:
            sstr=''
            sstr=sstr.join(element_array)
            process_begin=1
            current_state=0
            process_done=0
            process_valid=0
            next_state=0
            ap_done=0
            ap_idle=0
            ap_ready=0
            ap_vld=0
            if 'currentstate' in sstr:
                current_state=1
            if 'nextstate' in sstr:
                next_state=1
            if 'ap_done' in sstr:
                ap_done=1
            if 'ap_idle' in sstr:
                ap_idle=1
            if 'ap_ready' in sstr:
                ap_ready=1
            if 'ap_vld' in sstr:
                ap_vld=1
            if current_state==1 or next_state==1 or ap_done==1 or ap_idle==1 or ap_ready==1 or ap_vld==1:
                process_valid=0
            else:
                process_valid=1
            continue
        if process_begin==1 and process_done==0:
            if 'end' in element_array:
                if 'process;' in element_array:
                    process_done=1
                    process_begin=0
        if process_begin==1 and process_valid==0 and process_done==0:
            continue
        if process_begin==1 and process_valid==1 and process_done==0:
            if '<=' in element_array:
                base=element_array.index("<=")

                from_name=element_array[base+1][:len(element_array[base+1])-1]
                to_name=element_array[base-1]

                from_index_list=array_index_all(from_name)
                to_index_list=array_index_all(to_name)

                from_index=int(from_index_list[1],10)
                to_index=int(to_index_list[1],10)

                from_type=from_index_list[0]
                to_type=to_index_list[0]

                if from_type=='sarr':
                    signal_array[from_index].to=to_name
                if from_type=='parr':
                    port_array[from_index].to=to_name
                if from_type=='carr':
                    constant_array[from_index].to=to_name

                if to_type=='sarr':
                    signal_array[to_index].sfrom=from_name
                if to_type=='parr':
                    port_array[to_index].sfrom=from_name
                if to_type=='carr':
                    constant_array[to_index].sfrom=from_name

                #signal_array[from_index].to=to_name
                #signal_array[to_index].sfrom=from_name
        if process_done==1:
            if "<=" in element_array:
                base=element_array.index("<=")
                to_name=element_array[base-1]
                last=element_array[len(element_array)-1]
                last=last[:len(last)-1]
                element_array[len(element_array)-1]=last
                sstr=''
                sstr=sstr.join(element_array)
                sstr=remove(sstr,'std_logic_vector')
                sstr=remove(sstr,'unsigned')
                sstr=remove(sstr,'signed')
               # sstr=remove(sstr,'resize')

                if 'resize' in sstr:
                    paren_count=0
                    offset=0
                    incre=0
                    location=sstr.index('resize')+6
                    for character in sstr[location:]:
                        if incre==0:
                            offset=offset+1
                        if character=='(':
                            paren_count=paren_count+1
                        if character==')':
                            paren_count=paren_count-1
                        if paren_count==1 and offset!=1:
                            incre=incre+1
                        if paren_count<0:
                            break
                    sstr_l=sstr[:location-7]
                    sstr_m=sstr[location:location+offset]
                    sstr_r=sstr[location+offset+incre-1:]
                    sstr_list=[sstr_l,sstr_m,sstr_r]
                    sstr=''
                    sstr=sstr.join(sstr_list)
                 #   sstr=remove(sstr,'(')
                 #   sstr=remove(sstr,')')
                if '&' in sstr:
                    bb=sstr.index('&')
                    left=bb
                    right=bb
                    left_found=0
                    right_found=0
                    length_extend=1
                    while left_found==0:
                        left=left-1
                        if sstr[left]=='(':
                            left_found=1
                            break
                    while right_found==0:
                        right=right+1
                        if sstr[right]==')':
                            right_found=1
                            break
                    left_str=sstr[:left]
                    right_str=sstr[right:]
                    mid_str=sstr[left:right]
                    left_str=remove(left_str,'(')
                    left_str=remove(left_str,')')
                    right_str=remove(right_str,'(')
                    right_str=remove(right_str,')')
                    s_list=[left_str,mid_str,right_str]
                    sstr=''
                    sstr=sstr.join(s_list)
                else:
                    sstr=remove(sstr,'(')
                    sstr=remove(sstr,')')
                    length_extend=0
                if '+' in sstr or '-' in sstr or '*' in sstr:
                    complex_assignment=1
                else:
                    complex_assignment=0
                if complex_assignment==0:
                    base=element_array.index("<=")
                    from_name=element_array[base+1][:len(element_array[base+1])]

                    from_index_list=array_index_all(from_name)
                    to_index_list=array_index_all(to_name)

                    from_index=int(from_index_list[1],10)
                    to_index=int(to_index_list[1],10)

                    from_type=(from_index_list[0])
                    to_type=(to_index_list[0])

                    if from_type=='sarr':
                        signal_array[from_index].to=to_name
                    if from_type=='parr':
                        port_array[from_index].to=to_name
                    if from_type=='carr':
                        constant_array[from_index].to=to_name

                    if to_type=='sarr':
                        signal_array[to_index].sfrom=from_name
                    if to_type=='parr':
                        port_array[to_index].sfrom=from_name
                    if to_type=='carr':
                        constant_array[to_index].sfrom=from_name

                else:
                    oo=operator()
                    oo.operator_name('operator_'+str(operator_count))
                    op_name=('operator_'+str(operator_count))
                    operator_count=operator_count+1
                    if '+' in sstr:
                        oo.operator_type('+')
                        op_type='+'
                    if '-' in sstr:
                        oo.operator_type('-')
                        op_type='-'
                    if '*' in sstr:
                        oo.operator_type('*')
                        op_type='*'
                    op_base=sstr.index(op_type)
                    name0=sfrom0=sstr[len(to_name)+2:op_base]
                    sfrom1=sstr[op_base+1:]
                    oo.operator_to(to_name)
                    oo.operator_sfrom0(sfrom0)
                    oo.operator_sfrom1(sfrom1)
                    if length_extend==1:
                        name1=sfrom1[4:]
                    else:
                        name1=sfrom1
                    length0=array_update(name0,op_name,0)
                    length1=array_update(name1,op_name,0)+length_extend
                    op_length=max(length0,length1)
                    oo.operator_width(op_length)
                    array_update(to_name,op_name,1)
                    operator_array.append(oo)



fout.write('ENTITY NAME: '+entity_name+'\n')
for e1 in port_array:
    fout.write("PORT "+e1.name+" :{")
    fout.write("    DIRECTION: "+e1.direction)
    fout.write("    WIDTH: "+str(e1.width))
    fout.write("    TO: "+str(e1.to))
    fout.write("    FROM: "+str(e1.sfrom)+" }")
    fout.write("\n")
fout.write('\n')
for e2 in constant_array:
    fout.write("CONSTANT "+e2.name+" :{")
    fout.write("    WIDTH: "+str(e2.width))
    fout.write("    VALUE: "+str(e2.value))
    fout.write("    TO: "+str(e2.to)+" }")
    fout.write("\n")
fout.write('\n')
for e3 in signal_array:
    fout.write("SIGNAL "+e3.name+" :{")
    fout.write("    WIDTH: "+str(e3.width))
    fout.write("    TO: "+str(e3.to))
    fout.write("    FROM: "+str(e3.sfrom)+" }")
    fout.write("\n")
fout.write('\n')
for e4 in operator_array:
    fout.write('OPERATOR '+e4.name+' :{')
    fout.write('    WIDTH: '+str(e4.width))
    fout.write('    TYPE: '+str(e4.type))
    fout.write('    OPERAND1: '+str(e4.sfrom0))
    fout.write('    OPERAND2: '+str(e4.sfrom1))
    fout.write('    TO: '+str(e4.to)+' }')
    fout.write('\n')
