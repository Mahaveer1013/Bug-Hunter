import requests

class SQLInjectionTester:
    def __init__(self, forms):
        self.forms = forms
        self.sql_payloads = ["' OR '1'='1", "admin' --", "' OR 'a'='a"]

    def test_sql_injection(self):
        vulnerable_forms = []
        for form in self.forms:
            for payload in self.sql_payloads:
                data = {input["name"]: payload for input in form["inputs"] if input["name"]}
                response = requests.post(form["action"], data=data)
                if "sql" in response.text.lower() or "error" in response.text.lower():
                    vulnerable_forms.append(form)
                    break
        return vulnerable_forms
