# A class representing the state of a Video generation.

class VideoGenerationState:
    # shared across instances, per-line limit is 40.
    page_character_limit = 300


    def process(self):        
        i = 0
        while (i < len(self.lines)):
            curr_line = self.lines[i]
            while ((i + 1) < len(self.lines)):
                if ((len(curr_line) + len(self.lines[i + 1])) < self.page_character_limit):
                    i += 1
                    curr_line = curr_line + ' ' + self.lines[i]
                else:
                    break;

            if (len(curr_line) < 400):
                self.values.append(curr_line)
            else:
                raise Exception('Skipping Video generation for title ' + self.title)

            i += 1
                
        print "[DEBUG] Characters per page of video:"
        print map(len, self.values)


    def __init__(self, title, lines, bgcolor, accent, path_to_output):
        self.title = title
        self.lines = lines
        self.bgcolor = bgcolor
        self.accent = accent
        self.path_to_output = path_to_output
        
        self.values = []
        
        self.process()
        
    
