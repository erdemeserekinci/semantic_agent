from question_analyzer import NLPInterpreter

interpreter = NLPInterpreter()
info = interpreter.interpret_question("Who does Deepin belong to?")
print(info)