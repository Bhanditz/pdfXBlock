""" pdfXBlock main Python class"""

import os
import pkg_resources
from django.template import Context

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader


def _(str):
    """
    Dummy ugettext.
    """
    return str


@XBlock.needs('i18n')
class pdfXBlock(XBlock):
    """

    """

    loader = ResourceLoader(__name__)

    # Icon of the XBlock. Values : [other (default), video, problem]
    icon_class = "other"

    # Fields
    display_name = String(display_name=_("Display Name"),
        default=_("PDF"),
        scope=Scope.settings,
        help=_("This name appears in the horizontal navigation at the top of the page."))

    url = String(display_name=_("PDF URL"),
        default=_("http://tutorial.math.lamar.edu/pdf/Trig_Cheat_Sheet.pdf"),
        scope=Scope.content,
        help=_("The URL for your PDF."))
    
    allow_download = Boolean(display_name=_("PDF Download Allowed"),
        default=True,
        scope=Scope.content,
        help=_("Display a download button for this PDF."))
    
    source_text = String(display_name=_("Source document button text"),
        default="",
        scope=Scope.content,
        help=_("Add a download link for the source file of your PDF. Use it for example to provide the PowerPoint file used to create this PDF."))
    
    source_url = String(display_name=_("Source document URL"),
        default="",
        scope=Scope.content,
        help=_("Add a download link for the source file of your PDF. Use it for example to provide the PowerPoint file used to create this PDF."))

    def load_resource(self, resource_path):
        """
        Gets the content of a resource
        """
        resource_content = pkg_resources.resource_string(__name__, resource_path)
        return unicode(resource_content)

    def render_template(self, path, context=None):
        """
        Evaluate a template by resource path, applying the provided context
        """
        return self.loader.render_django_template(
            os.path.join("static/html", path),
            context=Context(context or {}),
            i18n_service=self.runtime.service(self, "i18n"),
        )

    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students
        when viewing courses.
        """
        
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'allow_download': self.allow_download,
            'source_text': self.source_text,
            'source_url': self.source_url
        }
        html = self.render_template('pdf_view.html', context)
        
        frag = Fragment(html)
        frag.add_css(self.load_resource("static/css/pdf.css"))
        frag.add_javascript(self.load_resource("static/js/pdf_view.js"))
        frag.initialize_js('pdfXBlockInitView')
        return frag

    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'allow_download': self.allow_download,
            'source_text': self.source_text,
            'source_url': self.source_url
        }
        html = self.render_template('pdf_edit.html', context)
        
        frag = Fragment(html)
        frag.add_javascript(self.load_resource("static/js/pdf_edit.js"))
        frag.initialize_js('pdfXBlockInitEdit')
        return frag

    @XBlock.json_handler
    def save_pdf(self, data, suffix=''):
        """
        The saving handler.
        """
        self.display_name = data['display_name']
        self.url = data['url']
        self.allow_download = True if data['allow_download'] == "True" else False # Str to Bool translation
        self.source_text = data['source_text']
        self.source_url = data['source_url']
        
        return {
            'result': 'success',
        }
