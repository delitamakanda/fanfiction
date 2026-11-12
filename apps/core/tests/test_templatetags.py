from django import forms
from django.template import Context, Template
from django.test import SimpleTestCase

from apps.core.markdown import render_user_markdown


class EmailForm(forms.Form):
    email = forms.EmailField()


class TemplateTagTests(SimpleTestCase):
    def render(self, source, **context):
        return Template(source).render(Context(context))

    def test_addclass_on_field_and_label(self):
        form = EmailForm()
        html = self.render(
            "{% load filters %}{{ form.email|addclass:'input' }}"
            "{{ form.email.label_tag|addclass:'label' }}",
            form=form,
        )
        self.assertIn('class="input"', html)
        self.assertIn('<label class="label"', html)

    def test_markdown_filters(self):
        html = self.render(
            "{% load markdown %}{{ text|markdown|safe }}", text="**gras**"
        )
        self.assertIn("<strong>gras</strong>", html)
        html = self.render(
            "{% load markdownify %}{{ text|show_markdown|safe }}", text="*it*"
        )
        self.assertIn("<em>it</em>", html)

    def test_gravatar(self):
        user = type("U", (), {"email": "Someone@Example.com "})()
        html = self.render("{% load gravatar %}{{ user|gravatar }}", user=user)
        self.assertTrue(html.startswith("https://www.gravatar.com/avatar/"))

    def test_user_markdown_escapes_raw_html(self):
        html = render_user_markdown("**ok** <script>alert(1)</script>")
        self.assertIn("<strong>ok</strong>", html)
        self.assertNotIn("<script>", html)
