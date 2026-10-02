from rtg_language import parse

source = '''
rtg "2.0";
object "Car" {
    instance "Chassis" as chassis;
}'''

ast, diagnostics = parse(source, "test.rtg")
print("Has errors:", diagnostics.has_errors())
for d in diagnostics:
    print(" ", d)
print("AST:", ast)