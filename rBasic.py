import sys

def fatal ( message ):
	print( "Fatal exception: " + message )
	exit( 1 )

file = sys.argv[ 1 ]
with open( file ) as contents:
	source = contents.readlines()


program = []
variables = {}


for line in source:
	line = line.strip()
	
	if line == "\n" : continue
	if line == "" : continue
	
	program.append( line.split( " " ) )


def get_str( line ):
	return " ".join( line )

def var_or_lit( literal ) :
	if literal in variables:
		return variables[ literal ]
	
	if type( literal ) == float or type( literal ) == int:
		return float( literal )
	
	if literal.isnumeric():
		return float( literal )
	else:
		return str( literal )

program_counter = 0

def execute():
	global program_counter
	line = program[ program_counter ]
	program_counter += 1
	
	match ( line[ 0 ] ):
		case "print":
			message = []
			
			for token in line[ 1: ]:
				if token[ 0 ] == "$":
					message.append( str( var_or_lit( token[ 1: ] ) ) )
				else:
					message.append( token )
				
			print( get_str( message ) )
		case "set":
			name = line[ 1 ]
			if len( line ) > 3:
				variables[ name ] = get_str( line[ 2: ] )
			else:
				variables[ name ] = var_or_lit( line[ 2 ] )
		case "for":
			index = line[ 1 ]
			inc = line[ 2 ]
			target = line[ 3 ]
			
			first_inst = program_counter
			last_inst = program_counter
			
			depth = 1
			for token_list in program[ program_counter: ]:
				
				if token_list[ 0 ] == "for":
					depth += 1;
				elif token_list[ 0 ] == "end":
					depth -= 1;
				
				if depth == 0 : break
				last_inst += 1
			
			while var_or_lit( index ) <= var_or_lit( target ):
				program_counter = first_inst
				for pc in range( first_inst, last_inst ):
					execute()
				
				if index in variables:
					variables[ index ] += var_or_lit( inc )
				else:
					index = float( index ) + var_or_lit( inc )
			
			program_counter = last_inst + 1
		
		case "if":
			pass
		
	if len( line ) <= 2:
		return
	
	match ( line[ 1 ] ):
		case "sum":
			name = line[ 0 ]
			sum = 0
			
			for literal in line[ 2: ]:
				value = var_or_lit( literal )
				if type( value ) != float:
					print( "Value of variable \"" + literal + "\" is" + str( var_or_lit( literal ) ) )
					fatal( "Line: " + ( " ".join( line ) ) + " | attempted to sum a non-number with a number!" )
				
				sum += value
			
			variables[ name ] = sum
		case "sub":
			name = line[ 0 ]
			sum = var_or_lit( line[ 2 ] )
			
			for literal in line[ 3: ]:
				value = var_or_lit( literal )
				if type( value ) != float:
					print( "Value of variable \"" + literal + "\" is" + str( var_or_lit( literal ) ) )
					fatal( "Line: " + ( " ".join( line ) ) + " | attempted to sum a non-number with a number!" )
				
				sum -= value
			
			variables[ name ] = sum
		
		case "mul":
			name = line[ 0 ]
			sum = var_or_lit( line[ 2 ] )
			
			for literal in line[ 3: ]:
				value = var_or_lit( literal )
				if type( value ) != float:
					print( "Value of variable \"" + literal + "\" is" + str( var_or_lit( literal ) ) )
					fatal( "Line: " + ( " ".join( line ) ) + " | attempted to ,m a non-number with a number!" )
				
				sum *= value
			
			variables[ name ] = sum

		case "div":
			name = line[ 0 ]
			sum = var_or_lit( line[ 2 ] )
			
			for literal in line[ 3: ]:
				value = var_or_lit( literal )
				if type( value ) != float:
					print( "Value of variable \"" + literal + "\" is" + str( var_or_lit( literal ) ) )
					fatal( "Line: " + ( " ".join( line ) ) + " | attempted to ,m a non-number with a number!" )
				
				sum /= value
			
			variables[ name ] = sum


print( program_counter )
while program_counter < len( program ):
	execute()


print( program, variables )
