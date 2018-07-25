import email


def getRecentMail(M):
    mailMap = {}

    typ, data = M.search(None, 'ALL')
   
    print typ
    ids = data[0]
    id_list = ids.split()

    #get the most recent email id
    latest_email_id = int( id_list[-1] )

    #iterate through 15 messages in decending order starting with latest_email_id
    #the '-1' parameter dictates reverse looping order
    for i in range( latest_email_id, latest_email_id-1, -1 ):
        typ, data = M.fetch( i, '(RFC822)' )

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part.__getitem__(1))
                varSubject = msg['subject']
                varFrom = msg['from']

                varFromName = varFrom.split("<")[0].strip().replace("\"", "")
                varFromId = varFrom.split("<")[1].replace(">", "").strip()

                bodytext=msg.get_payload()[0].get_payload()
                if type(bodytext) is list:
                    bodytext=','.join(str(v) for v in bodytext)

       
        #add ellipsis (...) if subject length is greater than 35 characters
        if len( varSubject ) > 35:
            varSubject = varSubject[0:32] + '...'

        if "MEGA" in varSubject :
            print '[' + varFromName + '...' + varFromId+ '] ' + varSubject + '\n' + bodytext
            
            mailMap['name'] = varFromName
            mailMap['email'] = varFromId
            mailMap['body'] = bodytext
    

    return mailMap
