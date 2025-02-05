file_to_read = "text2.print"
math_symbol = '+-*/%'
comparison_symbols = ['==', '>', '<', '>=', '<=']
state = {}


def varmap(var):
   if var in state:
       return state[var]
   else:
       raise NameError(f"Error: Variable '{var}' not found or defined")


def mathEval(expression):
   expression = expression.strip()
  
   if expression in state:
       return state[expression]
  
   for symbol in math_symbol:
       if symbol in expression:
           left, right = expression.split(symbol, 1)
           left = mathEval(left)
           right = mathEval(right)
          
           try:
               left = int(left)
               right = int(right)
           except ValueError:
               raise SyntaxError("Error: Invalid math expression")


           if symbol == '+':
               return left + right
           elif symbol == '-':
               return left - right
           elif symbol == '*':
               return left * right
           elif symbol == '/':
               return left / right
           elif symbol == '%':
               return left % right


   try:
       return int(expression)
   except ValueError:
       raise SyntaxError(f"Error: Invalid expression '{expression}' or variable not defined")


def conditionEval(expression):
   expression = expression.strip()
  
   if expression == "True":
       return True
   if expression == "False":
       return False
  
   for symbol in comparison_symbols:
       if symbol in expression:
           left, right = expression.split(symbol)
           left = mathEval(left.strip())
           right = mathEval(right.strip())
          
           if symbol == "==":
               return left == right
           elif symbol == ">":
               return left > right
           elif symbol == "<":
               return left < right
           elif symbol == ">=":
               return left >= right
           elif symbol == "<=":
               return left <= right


   raise SyntaxError(f"Error: Invalid condition '{expression}'")


def openFile(file_to_read):
   with open(file_to_read, "r") as file:
       whole_string = file.read()
       parser(whole_string)


def parser(statements):
   if isinstance(statements, str):
       statements = statements.strip().split('\n')
  
   i = 0
   skip_next_blocks = False


   while i < len(statements):
       line = statements[i].strip()


       if line.startswith("asgn: "):
           line = line.replace("asgn: ", "").strip()
           var, expr = line.split(" = ")
           expr = mathEval(expr)
           state[var.strip()] = expr




       elif line.startswith("p: "):
           line = line.replace("p:", "").strip()
           if line.startswith("\"") and line.endswith("\""):
               print(line[1:-1]) 
           else:
               value = mathEval(line)
               print(value)




       elif line.startswith('if: cnd(') and '~' in line:
           if not skip_next_blocks:
               condition = line[len('if: cnd('):line.index('~')].strip()[:-1]
               if conditionEval(condition):
                   body_start = i + 1
                   body_end = body_start
                   while body_end < len(statements) and statements[body_end].strip() != "~":
                       body_end += 1
                   body_statements = statements[body_start:body_end]
                   parser(body_statements)
                   i = body_end 
                   skip_next_blocks = True 
               else:
                   i += 1 
           else:
               i += 1


    
       elif line.startswith('elseif: cnd(') and '~' in line:
           if skip_next_blocks:
               i += 1
           else:
               condition = line[len('elseif: cnd('):line.index('~')].strip()[:-1]
               if conditionEval(condition):
                   body_start = i + 1
                   body_end = body_start
                   while body_end < len(statements) and statements[body_end].strip() != "~":
                       body_end += 1
                   body_statements = statements[body_start:body_end]
                   parser(body_statements) 
                   i = body_end 
                   skip_next_blocks = True 
               else:
                   i += 1


      
       elif line.startswith("else:"):
           if skip_next_blocks:
               i += 1
           else:
               body_start = i + 1
               body_end = body_start
               while body_end < len(statements) and statements[body_end].strip() != "~":
                   body_end += 1
               body_statements = statements[body_start:body_end]
               parser(body_statements)
               i = body_end 
               skip_next_blocks = True 


 
       elif line.startswith("for"):
           parts = line.split()
           var_name = parts[1]
           start = int(parts[3])
           end = int(parts[5])
          
           body_lines = []


        
           while i + 1 < len(statements):
               i += 1
               current_line = statements[i].strip()
               if current_line.startswith("next_for"):
                   break
               body_lines.append(current_line)


      
           if var_name not in state:
               print(f"Error: '{var_name}' not initialized before loop.")
               return


          
           for j in range(start, end + 1):
               state[var_name] = j
               parser(body_lines) 


        elif line.startswith("while: "):
           condition = line.replace("while: ", "").strip()
          
           body_lines = []


         
           while i + 1 < len(statements):
               i += 1
               current_line = statements[i].strip()
               if current_line.startswith("next_while"):
                   break
               body_lines.append(current_line)
          
           while conditionEval(condition):
               parser(body_lines) 


 
       elif "=" in line:
           var, expr = line.strip().split("=")
           expr = mathEval(expr.strip())
           state[var.strip()] = expr


       i += 1


openFile(file_to_read)
