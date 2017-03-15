import requests, os, argparse, re, ast,sys


class ExtGuesser():

    extensions = None

    def __init__(self, arguments):
        self.verify_arguments(arguments)
        self.check_extensions(arguments)

    def verify_arguments(self,arguments):
        if arguments.extension_file:
            self.extensions = self.parse_file(arguments.extension_file)
            return

        if arguments.extensions:
            self.extensions = re.split(",", arguments.extensions)
            return

        print "Extensions not provided! Quitting"
        sys.exit(0)

    def preprocess_paths(self, paths):
        processed_paths = []
        for path in paths:
            processed_paths.append(path)
            split = re.split("\.", path)
            if len(split) > 1:
                processed_paths.append(split[0])

            #break paths into all their subdirectories (/bla/blue/bli => [/bla/, bla/blue,/bla/blue/bli]
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
        results = []
        headers = None
        if arguments.headers:
            headers = ast.literal_eval(arguments.headers)

        paths = self.parse_file(arguments.paths_file)
        processed_paths = self.preprocess_paths(paths)
        print "processed_paths: " + str(processed_paths)

        i = 0
        for path in processed_paths:
            for ext in self.extensions:
                req_url = arguments.url + path + "." + ext

                response = requests.get(req_url,headers=headers,allow_redirects=False)
                if arguments.verbose:
                    print str(response.status_code) + " from " + path + "." + ext

                if response.status_code == 200:
                    print "Found: " + str(response.status_code) + " from " + path + "." + ext
                    results.append(path + "." + ext)

            i = i + 1
            completed_precentage = 100*float(i)/float(len(processed_paths))
            print "Completed " + str(completed_precentage) + "%"

        print "Scan completed! Results:"
        for result in results:
            print result


    def parse_file(self, path):
        with open(path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        #print content
        return content


parser = argparse.ArgumentParser(description='Parse')
parser.add_argument("-u", "--url", help="The url to check", required=True)
parser.add_argument("-e", "--extension-file", help="Path of extension file")
parser.add_argument("-E", "--extensions", help="List of extensions")
parser.add_argument("-p", "--paths-file", help="Path of paths file", required=True)
parser.add_argument("-H", "--headers", help="Headers in JSON format")
parser.add_argument("-v", "--verbose", help="Be verbose",action='store_true')

args = parser.parse_args()

checker = ExtGuesser(args)
