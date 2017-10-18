from bottle import route,run,Bottle,template,request
app=Bottle()
program_data=''
program_list=[]
input_tape=[]
current_state=''#TM STATE
accept_states=[]#accepting states
current_position=0#TM HEAD POSITION
output_file=''
def write_output_file():
	file3=open(output_file,'a+')
	temp=''
	for p in input_tape:
		temp=str(temp)+p+' '
	temp=temp+'-------------- '+str(current_state)+' '+str(current_position)
	file3.write(temp+str('\n'))
	file3.close()
@app.route('/')
def home():
	global program_data
	global program_list
	global input_tape
	global current_state
	global accept_states
	global current_position
	global output_file
	program_data=''
	program_list=[]
	input_tape=[]
	current_state=''
	accept_states=[]
	current_position=1
	output_file=''
        return template('home')
@app.post('/instructions')
def instructions():
    return template('instructions')
@app.post('/program_page')
def program_page():
	return template('program_page')
#page 1 program
@app.post('/get_program_data')
def get_program_data():
#program_data='testprog.pgtm\nB q p\nq X p Y r\nq B q B r'
	global program_data
	global program_list
	global current_state
	global accept_states
	program_data=''
	program_data=request.forms.get('program')
	program_list=program_data.split('\n')
	file1=open(program_list[0][:-1],'w')
	count=0
	for k in program_list:
		print k
		if count==0 :
			count=count+1
			continue
		file1.write(k+'\n')
	file1.close()
	count=0
	program_list[1]=program_list[1].split('\r')[0]
	current_state=program_list[1].split(' ')[1]
	accept_states=program_list[1].split(' ')[2:]
	print(current_state)
	print(accept_states)
	print(program_data)
	print(program_list)
	return template('input_page')
@app.post('/get_program_file')
def get_program_file():
	global program_data
        global program_list
	global current_state
	global accept_states
	count=0
	program_data=''
	program_list=[]
	temp=request.forms.get('filename')
	file2=open(temp,'r+')
	program_list.append(temp)
	for k in file2.read():
		if count==0:
			count+=1
			program_data=k
		else:
			program_data=program_data+k
        for k in program_data.split('\n'):
		program_list.append(k)
#	print 'hi'+str(program_list)
	del program_list[-1]
	program_list[1]=program_list[1].split('\r')[0]
        current_state=program_list[1].split(' ')[1]
        accept_states=program_list[1].split(' ')[2:]
	print(current_state)
        print(accept_states)
        print(program_data)
        print(program_list)
	return template('input_page')
#page 2 input
@app.post('/get_input')
def get_input():
	global output_file
	global input_tape
	global current_position
	global current_state
	input_tape=request.forms.get('input')	
	input_tape=input_tape.split(' ')
	print(input_tape)
	output_file=request.forms.get('outputfile')
	print current_state
	write_output_file()
	return template('simulate',iptp=input_tape,cp=current_position,cs=current_state)
@app.post('/get_input_file')
def get_input_file():
	global output_file
	global input_tape
	global current_position
	global current_state
	count=0
	input_tape=[]
	file3=open(request.forms.get('inputfile'),'r')
        for k in file3.read():
		if (ord(k)>=65 and ord(k)<=90) or (ord(k)>=48 and ord(k)<=57):
				input_tape.append(k)
        print(input_tape)
	output_file=request.forms.get('outputfile')
	print current_state
	write_output_file()
	return template('simulate',iptp=input_tape,cp=current_position,cs=current_state,temp=' ')
#page 3 simulate
def one_step():
	global current_state
	global current_position
	global input_tape
	flag=False
	count=0
	for k in program_list:
		if count<2:
			count+=1
			continue
		transition_list=k.split('\r')
		transition_list=transition_list[0].split(' ')
		print(transition_list)
		if(transition_list[0]==current_state and transition_list[1]==input_tape[current_position]):
			flag=True
			input_tape[current_position]=transition_list[3]
			if(transition_list[4]=='l'):
				current_position-=1
			else:
				current_position+=1
			current_state=transition_list[2]
			print(input_tape)
			return flag
	return flag
#one_step()
#one_step()
#one_step()
#print(current_position)
@app.post('/next_step')
def next_step():
	k=one_step()
	if k==True:
		write_output_file()			
	return template('simulate',iptp=input_tape,cp=current_position,cs=current_state,temp=' ')
@app.post('/proceed')
def proceed():
	one_step()
        global current_state
        global current_position
        global input_tape
	global accept_states
	while True:
		if current_state in accept_states :
			return template('simulate',iptp=input_tape,cp=current_position,cs=current_state,temp=' ')
		else:
			k=one_step()
			if(k==False):
				return template('simulate',iptp=input_tape,cp=current_position,cs=current_state,temp=' ')
			else:
				write_output_file()
run(app,host ='localhost',port=7777,debug=True)
