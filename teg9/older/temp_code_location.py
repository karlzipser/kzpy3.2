

replace_dic = {"REPO",REPO},{"CAF",CAF},{"MODEL",MODEL}
rd = replace_dic
sr = str_replace

exec(sr("import REPO.CAF.MODEL.solver as Solver",rd))

exec(sr("from REPO.utils import *",rd))

exec(sr("import REPO.CAF.protos as protos",rd))

