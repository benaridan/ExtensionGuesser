import requests, os, argparse, re


class ExtGuesser():

    def __init__(self, arguments):
        self.check_extensions(arguments)



    def preprocess_paths(self, paths):
        processed_paths = []
        for path in paths:
            processed_paths.append(path)
            split = re.split("\.", path)
            if len(split) > 1:
                processed_paths.append(split[0])

            #break paths into all their subdirectories (/bla/blue/ => [/bla/, bla/blue]
            for m in re.finditer("/", path):
                start = m.start()
                end = m.end()
                if start > 0:
                    processed_paths.append(path[:start])

        #to make the list unique
        uniq_set = set(processed_paths)
        processed_paths = list(uniq_set)
        return processed_paths

    def check_extensions(self, arguments):
        extensions = self.parse_file(arguments.extension_file)
        paths = self.parse_file(arguments.paths_file)
        processed_paths = self.preprocess_paths(paths)
        print "processed_paths: " + str(processed_paths)

        for path in processed_paths:
            for ext in extensions:
                req_url = arguments.url + path + "." + ext
                response = requests.head(req_url)
                if response.status_code == 200:
                    print str(response.status_code) + " from " + path + "." + ext

    def parse_file(self, path):
        with open(path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        print content
        return content


parser = argparse.ArgumentParser(description='Parse')
parser.add_argument("-u", "--url", help="The url to check", required=True)
parser.add_argument("-e", "--extension-file", help="Path of extension file", required=True)
parser.add_argument("-p", "--paths-file", help="Path of paths file", required=True)
args = parser.parse_args()

checker = ExtGuesser(args)
