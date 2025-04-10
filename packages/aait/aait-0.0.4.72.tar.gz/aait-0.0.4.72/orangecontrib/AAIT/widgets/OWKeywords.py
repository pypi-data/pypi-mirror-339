import os
import sys

from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output
from Orange.data import Table, Domain, StringVariable, ContinuousVariable
from thefuzz import fuzz
from AnyQt.QtWidgets import QApplication

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils.import_uic import uic
    from Orange.widgets.orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file
else:
    from orangecontrib.AAIT.utils.import_uic import uic
    from orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file

@apply_modification_from_python_file(filepath_original_widget=__file__)
class OWKeywords(widget.OWWidget):
    name = "Keywords Detection"
    description = "Give the amount of keywords from in_object in in_data"
    icon = "icons/keyword.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/keyword.png"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owkeyword.ui")
    want_control_area = False
    priority = 1050

    class Inputs:
        data = Input("Content", Table)
        keywords = Input("Keywords", Table)

    class Outputs:
        data = Output("Keywords per Content", Table)

    def __init__(self):
        super().__init__()
        self.data = None
        self.keywords = None
        self.setFixedWidth(470)
        self.setFixedHeight(300)
        uic.loadUi(self.gui, self)
        self.autorun = True

    @Inputs.data
    def set_data(self, in_data):
        self.data = in_data
        if self.autorun and self.keywords:
            self.process()

    @Inputs.keywords
    def set_keywords(self, in_keywords):
        self.keywords = in_keywords
        if self.autorun and self.data:
            self.process()

    def fuzzy_match_keywords(self, text, keyword_list, threshold=80):
        matched_keywords = []
        words = text.split(" ")
        for keyword in keyword_list:
            for word in words:
                if fuzz.ratio(word.lower(), keyword.lower()) >= threshold:
                    matched_keywords.append(keyword)
                    break
        return matched_keywords

    def process(self):
        if self.data is None or self.keywords is None:
            print("[INFO] No input data or keywords provided.")
            return

        if "Content" not in self.data.domain:
            self.error("Missing 'Content' column in input data")
            print("[ERROR] 'Content' column not found in input data.")
            return

        self.error("")  # Clear previous errors

        # Extract keywords from the 'Keywords' column
        try:
            if "Keywords" not in self.keywords.domain:
                self.error("Missing 'Keywords' column in keywords table")
                print("[ERROR] 'Keywords' column not found in keyword input.")
                return

            keyword_list = [str(row["Keywords"]) for row in self.keywords if str(row["Keywords"]).strip() != ""]
            print(f"[INFO] Extracted {len(keyword_list)} keywords: {keyword_list}")
        except Exception as e:
            self.error("Error while extracting keywords")
            print(f"[EXCEPTION] Failed to extract keywords: {e}")
            return

        new_strings = list(self.data.domain.metas)
        if not any(var.name == "Keywords_Detected" for var in new_strings):
            new_strings = new_strings + [StringVariable("Keywords_Detected")]
        if not any(var.name == "Keywords_Count" for var in new_strings):
            new_strings = new_strings + [ContinuousVariable("Keywords_Count")]

        new_domain = Domain(self.data.domain.attributes,
                            self.data.domain.class_vars,
                            new_strings)

        new_metas = []
        for i, row in enumerate(self.data):
            text = str(row["Content"])
            matched = self.fuzzy_match_keywords(text, keyword_list)
            matched_str = ", ".join(matched)
            matched_count = len(matched)
            print(f"[DEBUG] Row {i}: Matched {matched_count} keywords -> {matched_str}")
            new_metas.append(list(row.metas) + [matched_str, matched_count])

        out_data = Table(new_domain, self.data.X, self.data.Y, new_metas)
        print("[INFO] Process complete. Sending output data.")
        self.Outputs.data.send(out_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ow = OWKeywords()
    ow.show()
    app.exec_()
