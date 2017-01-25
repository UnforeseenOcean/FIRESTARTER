###############################################################################
# FIRESTARTER - A Processor Stress Test Utility
# Copyright (C) 2017 TU Dresden, Center for Information Services and High
# Performance Computing
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: daniel.hackenberg@tu-dresden.de
###############################################################################

def list_functions(file,architectures,templates):
    id = 0
    for each in architectures:
        for isa in each.isa:
            for tmpl in templates:
                if ("ISA_"+isa.upper() == tmpl.name) and (tmpl.win64_incl == 1):
                    for threads in each.threads:
                        id = id + 1
                        func_name = 'func_'+each.arch+'_'+each.model+'_'+isa+'_'+threads+'T'
                        file.write("  printf(\"  %4.4s | %.30s \\n\",\""+str(id)+"\",\""+func_name.upper()+"                             \");\n")

def get_function_cases(file,architectures,templates):
    id = 0
    for each in architectures:
        for isa in each.isa:
            for tmpl in templates:
                if ("ISA_"+isa.upper() == tmpl.name) and (tmpl.win64_incl == 1):
                    for threads in each.threads:
                        id = id + 1
                        func_name = 'func_'+each.arch+'_'+each.model+'_'+isa+'_'+threads+'t'
                        file.write("       case "+str(id)+":\n")
                        file.write("         func = "+func_name.upper()+";\n")
                        file.write("         break;\n")

def thread_definitions(file,architectures,templates):
    for each in architectures:
        for isa in each.isa:
            for tmpl in templates:
                if ("ISA_"+isa.upper() == tmpl.name) and (tmpl.win64_incl == 1):
                    for threads in each.threads:
                        func_name = each.arch+'_'+each.model+'_'+isa+'_'+threads+'t'
                        file.write("static DWORD WINAPI FUNC_"+func_name.upper()+"_Thread(void* threadParams)\n")
                        file.write("{\n")
                        file.write("  threaddata_t * data = malloc(sizeof(threaddata_t));\n")
                        if (int(threads) == 1):
                            file.write("  void * p= _mm_malloc(13406208*8,4096);\n")
                        if (int(threads) == 2):
                            file.write("  void * p= _mm_malloc(6703104*8,4096);\n")
                        if (int(threads) == 4):
                            file.write("  void * p= _mm_malloc(3351552*8,4096);\n")
                        file.write("\n")
                        file.write("  data->addrMem = (unsigned long long) p;\n")
                        file.write("  data->addrHigh = (unsigned long long) &HIGH;\n")
                        file.write("  init_"+func_name+"(data);\n")
                        file.write("  asm_work_"+func_name+"(data);\n")
                        file.write("  return 0;\n")
                        file.write("}\n")

def start_threads(file,architectures,templates):
    for each in architectures:
        for isa in each.isa:
            for tmpl in templates:
                if ("ISA_"+isa.upper() == tmpl.name) and (tmpl.win64_incl == 1):
                    for threads in each.threads:
                        func_name = 'func_'+each.arch+'_'+each.model+'_'+isa+'_'+threads+'t'
                        file.write("    case "+func_name.upper()+":\n")
                        file.write("      printf(\"\\nTaking "+isa.upper()+" code path optimized for "+each.name+" - "+threads+" thread(s) per core\\n\");\n")
                        file.write("      for (i=0;i<nr_threads;i++){\n")
                        file.write("          threads[i]=CreateThread(\n")
                        file.write("              NULL,\n")
                        file.write("              0,\n")
                        file.write("              "+func_name.upper()+"_Thread,\n")
                        file.write("              NULL,\n")
                        file.write("              0,\n")
                        file.write("              &threadDescriptor);\n")
                        file.write("      }\n")
                        file.write("      break;\n")

