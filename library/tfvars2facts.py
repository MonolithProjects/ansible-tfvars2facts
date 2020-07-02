
# Copyright: (c) 2020, Michal Muransky <michal.muransky@pan-net.eu>
# MIT License (see COPYING or https://mit-license.org/)

DOCUMENTATION = '''
---
module: my_test

short_description: This is my test module

version_added: "2.4"

description:
    - "This is my longer description explaining my test module"

options:
    name:
        description:
            - This is the message to send to the test module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

extends_documentation_fragment:
    - azure

author:
    - Your Name (@yourhandle)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_test:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
    returned: always
message:
    description: The output message that the test module generates
    type: str
    returned: always
'''

import io
import jinja2
import re

from ansible.module_utils.basic import AnsibleModule

def run_module():

    global module

    module = AnsibleModule(
        argument_spec=dict(
            tfvars=dict(type='path', default='./vars.tfvars'),
            facts=dict(type='path', default='/tmp/tfars2facts.json'),
        ),
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    if module.check_mode:
        module.exit_json(**result)

    tfvars = module.params['tfvars']
    facts = module.params['facts']

    tmp = process_tfvars(tfvars)
    tmp = render_template(tmp)
    write_ouptut(facts, tmp)

    result['changed'] = True
    if module.params['tfvars'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)
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
