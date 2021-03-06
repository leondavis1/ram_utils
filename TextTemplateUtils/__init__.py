__author__ = 'm'

# import shutil
import os
import re

def replace_template(template_file_name,out_file_name, replace_dict={}):

    # out_file_name,ext = os.path.splitext(template_file_name)

    in_file = open(template_file_name,'r')
    out_file = open(out_file_name,'w')

    for line in in_file.readlines():
        line = line.rstrip()
        new_line_tmp = str(line)
        for name_in_template, replace_val in replace_dict.iteritems():
            # new_line_tmp = re.sub(name_in_template,replace_val,new_line_tmp)
            # using lambda function in the replace string to make sure that escaped characters such as \n \r \b are
            # not being interpreted but treated literarly
            repl_fcn = lambda x:str(replace_val)
            new_line_tmp = re.sub(pattern=name_in_template, repl=repl_fcn, string=new_line_tmp)

            # new_line_tmp = re.sub(pattern=name_in_template, repl=replace_val.encode('string-escape'),string=new_line_tmp)


            new_line_tmp = new_line_tmp.rstrip()
            #print 'newLineTmp=',newLineTmp

        print>>out_file,new_line_tmp

    in_file.close()
    out_file.close()
    # os.remove(template_file_name)

def replace_template_to_string(template_file_name,replace_dict={}):


    out_str = ''
    in_file = open(template_file_name,'r')


    for line in in_file.readlines():
        line = line.rstrip()
        new_line_tmp = str(line)
        for name_in_template, replace_val in replace_dict.iteritems():
            # new_line_tmp = re.sub(name_in_template,replace_val,new_line_tmp)
            # using lambda function in the replace string to make sure that escaped characters such as \n \r \b are
            # not being interpreted but treated literarly
            repl_fcn = lambda x:str(replace_val)
            new_line_tmp = re.sub(pattern=name_in_template, repl=repl_fcn, string=new_line_tmp)

            # new_line_tmp = re.sub(pattern=name_in_template, repl=replace_val.encode('string-escape'),string=new_line_tmp)


            new_line_tmp = new_line_tmp.rstrip()
            #print 'newLineTmp=',newLineTmp
        out_str += new_line_tmp+'\n'
        # print>>out_file,new_line_tmp

    in_file.close()
    return out_str

