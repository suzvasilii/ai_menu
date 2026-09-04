def getAuthResult(auth_type:str, success:bool, detail: str ="") -> str:
    text = auth_type
    if success:
        text += " completed successfully!"
    else:
        text += " error."
    if detail:
        text += f" Detail:{detail}."
    return text

def getFindImageResult(success:bool, detail: str="") -> str:
    text = "Http request"
    if success:
        text += " completed successfully. Image found!"
    else:
        text += " completed with error"
    if detail:
        text+= f" Detail:{detail}."
    return text

def returnBadrequestError(detail: str)-> str:
    return f"Invalid data sent, please re-check your data. Detail: {detail}."