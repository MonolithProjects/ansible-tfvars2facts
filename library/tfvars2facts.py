
# Copyright: (c) 2020, Michal Muransky <michal.muransky@pan-net.eu>
# MIT License (see COPYING or https://mit-license.org/)

from ansible.module_utils._text import to_bytes, to_native
DOCUMENTATION = r'''
---
module: tfvars2facts

short_description: Translate the Terraform tfvrs file to Ansible Local Facts (JSON).

version_added: "2.4"

description:
    - This Ansible module translates the Terraform tfvrs file to Ansible Local Facts.
    - Use the C(tfvars2facts) module if you want to use Terraform variables from tfvars in the Ansible.
    - You can run this module locally and copy the output JSON file to /etc/ansib.e/facts.d/ directory
      on the destination host.

options:
    src:
        description:
            - This is path to the tfvars file
            - This can be absolute or relative.
        required: true
        default: ./vars.tfvars
    dest:
        description:
            - Path and file name for the JSON output.
        required: true
        default: ./tfars.json

seealso:
- module: copy

author:
    - Michal Muransky (michal.muransky@pan-net.eu)
'''

EXAMPLES = r'''
- name: Run the translation on the runner
  tfvars2facst:
    src: /home/myuser/vars.tfvars
    dest: /tmp/tfvars.json
  delegate_to: localhost
  run_once: yes
'''

RETURN = '''
message:
    description: Terraform tfvars translated to Ansible Local Facts
    type: str
    returned: always
'''

import io
import jinja2
import os
import re
import time

from ansible.module_utils.basic import AnsibleModule

def run_module():

    global module

    module = AnsibleModule(
        argument_spec=dict(
            src=dict(type='path', default='./vars.tfvars'),
            dest=dict(type='path', default='./tfars.json'),
        ),
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        message='Terraform tfvars translated to Ansible Local Facts'
    )
    
    tfvars = module.params['src']
    facts = module.params['dest']
    if not os.path.exists(tfvars):
        module.fail_json(
            msg="Terraform tfvars file %s not found" % (tfvars))
    tmp = process_tfvars(tfvars)
    tmp = render_template(tmp)
    if not module.check_mode:
        if os.path.isfile(facts):
            if tmp == open(facts).read():
                result['changed'] = False
                module.exit_json(**result)
        write_ouptut(facts, tmp)
        if module.params['dest']:
            modified = os.stat(facts).st_mtime
            now = time.time()
            if (modified - now) < 1:
                result['changed'] = True
            else:
                result['changed'] = False
                module.fail_json(msg='Temporarry Ansible Local Facts file was not generated.', **result)
    module.exit_json(**result)


def process_tfvars(tfvars):
    output = io.StringIO()
    tfvars = open(tfvars)
    for line in tfvars.readlines():
        # Continue if the line is not commented or empty
        if re.match('#(?:.*)+|^(?:[\t ]*(?:\r?\n|\r))+', line) is None:
            # Remove commnets after the lines
            line = re.sub(r'#.*$', "", line)
            # Replace dash by underscore in var names
            line = re.sub(r'-(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)', '_', line)
            # Place var names inside the quotes
            line = re.sub(r'(^[\w\d_]+)', r'"\1"', line)
            # Replace symbol equal by colon
            line = re.sub(r'\s*=\s*', ': ', line)
            output.write(line)
    output = output.getvalue()
    return output

def render_template(data):
    template_body = '''
{
    {%+ for line in lines %}{{ line }}{% if not loop.last %},
    {% endif %}{%- endfor %} 
}
    '''
    lines = data.splitlines()
    template = jinja2.Template(template_body)
    output = template.render(lines=lines)
    return output

def write_ouptut(facts, output_data):
    with open(facts, "w") as output_file:
        for line in output_data:
            output_file.write(line)

def main():
    run_module()

if __name__ == '__main__':
    main()
