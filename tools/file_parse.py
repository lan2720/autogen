from opencc import OpenCC


def tc_to_sc(text):
    """Convert Traditional Chinese text to Simplified Chinese text.

    :param text: string, required. Only input parameter for the function. It is a string in Traditional Chinese that you want to convert to Simplified Chinese.
    :return: [description]
    :rtype: [type]
    """
    cc = OpenCC('t2s')
    simplified_text = cc.convert(text)
    return simplified_text