import sublime, sublime_plugin
import os
import subprocess

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class EasyHtmlWindowCmd(sublime_plugin.WindowCommand):
    def getTemplateRepoPath(self):
        s = sublime.load_settings("Preferences.sublime-settings")
        return s.get("template_path", "templates")

class EasyHtmlUpdateTemplatesCommand(EasyHtmlWindowCmd):
    def run(self):
        ipp = sublime.packages_path()
        templates_dir = os.path.join(
            ipp,
            self.getTemplateRepoPath()
        )

        try:
            with cd( templates_dir ):
                subprocess.check_output(
                    ['git', 'pull'],
                    stderr=subprocess.STDOUT
                )
        except subprocess.CalledProcessError as e:
            # We managed to call git, but it exited non-zero
            # e.returncode and e.output will be of interest
            sublime.set_clipboard(e.output.decode(encoding='UTF-8'))
            self.__bailOut()
        except Exception as e:
            sublime.error_message("Failed to update templates.  E-mail Mike.")

    def __bailOut(self):
        sublime.error_message("Failed to update templates.  E-mail Mike, "
                "including the contents of the clibpard.")

class EasyHtmlNewEmailCommand(EasyHtmlWindowCmd):
    def run(self):
        w    = self.window
        view = w.new_file()

        view.set_syntax_file('Packages/HTML/HTML.tmLanguage')
        w.run_command("insert_snippet", {
            # Yes, this needs to be "/".join, not os.path.join.
            "name": "/".join([
                "Packages",
                self.getTemplateRepoPath(),
                "html-email.sublime-snippet"
            ])
        })
