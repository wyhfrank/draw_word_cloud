from nlp_lib import *

input_file = "./data/mao_jp.txt"
cleaned_file = "./output/cleaned.txt"
mecab_file = "./output/mecab.txt"
post_file = "./output/post.txt"
# post_file = "./output/test.txt"


def main():
    print "Start pre-processing..."
    Preprocessing(input_file, outFile=cleaned_file)
    print "Calling mecab..."
    call_mecab(cleaned_file, mecab_file)
    print "Start post-processing..."
    PostProcess(mecab_file, post_file, [])
    print "Start drawing..."
    GenerateTagCloud(post_file)
    print "Done."


def test():
    call_mecab(cleaned_file, mecab_file)


if __name__ == '__main__':
    main()
    # test()
    # GenerateTagCloud(post_file)
