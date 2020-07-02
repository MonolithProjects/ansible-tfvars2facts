
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

def backup():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
