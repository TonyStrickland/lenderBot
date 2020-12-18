
import Conan.slackUtils as slackUtils
from Conan.slackUtils import Command as Command
import Conan.parseUtils as parseUtils
import Conan.lendingLibraryAdapter as adapter
import Conan.data.comments as comments

published = []

class AllFacts(Command):
    def __init__(self):
        super().__init__(source = AllFacts, method = self.getAllFacts, name = ['AllFacts', 'Facts'])

    def getAllFacts(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                parsed = parseUtils.parseFact_select()
                slackUtils.inChannelResponse(client, channel, parsed)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(AllFacts())

class AddFact(Command):
    def __init__(self):
        super().__init__(source = AddFact, method = self.addFact, name = ['AddFact', 'addf'])

    def addFact(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                mediaInfo = text[len(args[0])+1:].strip().capitalize()
                if len(mediaInfo) > 10:
                    sqlResult = adapter.insert_Fact(mediaInfo)
                    if not sqlResult:
                        slackUtils.inChannelResponse(client, channel,"""I had forgotten about that! I'll begin telling this tale when asked for more:\n{}""".format(mediaInfo))
                        return
                    slackUtils.inChannelResponse(client, channel, comments.notEnough)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(AddFact())

class RemoveFact(Command):
    def __init__(self):
        super().__init__(source = RemoveFact, method = self.removeFact, name = ['RemoveFact', 'remf'])

    def removeFact(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                someID = text[len(args[0])+1:].strip()
                if someID:
                    exists = adapter.getFactByID(someID)
                    if exists != -1 and exists:
                        if not adapter.remove_Facts(someID):
                            slackUtils.inChannelResponse(client, channel, comments.removeItem.format(exists)) ## TODO format this properly to remove Fact
                            return
                        slackUtils.inChannelResponse(client, channel, comments.notFound3)
                        return
                    slackUtils.inChannelResponse(client, channel, comments.doesntExist)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(RemoveFact())

class AllInsults(Command):
    def __init__(self):
        super().__init__(source = AllInsults, method = self.getAllInsults, name = ['AllInsults', 'Insults'])

    def getAllInsults(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                parsed = parseUtils.parseInsult_select()
                slackUtils.inChannelResponse(client, channel, parsed)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(AllInsults())

class AddInsult(Command):
    def __init__(self):
        super().__init__(source = AddInsult, method = self.addInsult, name = ['AddInsult', 'addi'])

    def addInsult(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                mediaInfo = text[len(args[0])+1:].strip().capitalize()
                if len(mediaInfo) > 10:
                    sqlResult = adapter.insert_Fact(mediaInfo)
                    if not sqlResult:
                        slackUtils.inChannelResponse(client, channel,"""That's a good one! I'll make sure to remember to hurl this at those who displease me:\n{}""".format(mediaInfo))
                        return
                    slackUtils.inChannelResponse(client, channel, comments.notEnough)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(AddInsult())

class RemoveInsult(Command):
    def __init__(self):
        super().__init__(source = RemoveInsult, method = self.removeInsult, name = ['RemoveInsult', 'remi'])

    def removeInsult(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                someID = text[len(args[0])+1:].strip()
                if someID:
                    exists = adapter.getInsultByID(someID)
                    if exists != -1 and exists:
                        if not adapter.remove_Insults(someID):
                            slackUtils.inChannelResponse(client, channel, comments.removeItem.format(exists)) ## TODO format this properly to remove Fact
                            return
                        slackUtils.inChannelResponse(client, channel, comments.notFound3)
                        return
                    slackUtils.inChannelResponse(client, channel, comments.doesntExist)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(RemoveInsult())

class AddMediaType(Command):
    def __init__(self):
        super().__init__(source = AddMediaType, method = self.addMediaType, name = ['AddMediaType', 'amt'])

    def addMediaType(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                mediaInfo = text[len(args[0])+1:].strip().capitalize()
                if len(mediaInfo) > 4 and len(mediaInfo) < 20:
                    sqlResult = adapter.insert_MediaType(mediaInfo)
                    if not sqlResult:
                        slackUtils.inChannelResponse(client, channel,"""I'll add "{}" to the types of media carried by the backs of our enemies!""".format(mediaInfo))
                        return
                    slackUtils.inChannelResponse(client, channel, comments.notEnough)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(AddMediaType())

class AddMediaCategory(Command):
    def __init__(self):
        super().__init__(source = AddMediaCategory, method = self.addMediaCategory, name = ['AddMediaCategory', 'amc'])

    def addMediaCategory(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                mediaInfo = text[len(args[0])+1:].strip().capitalize()
                if len(mediaInfo) > 4 and len(mediaInfo) < 20:
                    sqlResult = adapter.insert_MediaCategory(mediaInfo)
                    if not sqlResult:
                        slackUtils.inChannelResponse(client, channel,"""I'll add "{}" to the types of media carried by the backs of our enemies!""".format(mediaInfo))
                        return
                    slackUtils.inChannelResponse(client, channel, comments.notEnough)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(AddMediaCategory())

class AddMedia(Command):
    def __init__(self):
        super().__init__(source = AddMedia, method = self.addMedia, name = ['AddMedia', 'add'])

    def addMedia(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                mediaInfo = text[len(args[0])+1:].strip().capitalize()
                if mediaInfo:
                    parsed, mediaName = parseUtils.parseMedia_insert(mediaInfo)
                    sqlResult = adapter.insert_Media(parsed)
                    if not sqlResult:
                        slackUtils.inChannelResponse(client, channel, comments.adding.format(mediaName))
                        return
                    slackUtils.inChannelResponse(client, channel, comments.notEnough)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(AddMedia())

class RemoveMedia(Command):
    def __init__(self):
        super().__init__(source = RemoveMedia, method = self.removeMedia, name = ['RemoveMedia', 'remove'])

    def removeMedia(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                someID = text[len(args[0])+1:].strip()
                if someID:
                    exists = adapter.select_MediaID(someID)
                    if exists != -1 and exists:
                        if not adapter.remove_Media(someID):
                            slackUtils.inChannelResponse(client, channel, comments.removeItem.format(exists[0][4]))
                            return
                        slackUtils.inChannelResponse(client, channel, comments.notFound3)
                        return
                    slackUtils.inChannelResponse(client, channel, comments.doesntExist)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)
        
published.append(RemoveMedia())

class UpdateMediaCategory(Command):
    def __init__(self):
        super().__init__(source = UpdateMediaCategory, method = self.updateMediaCategory, name = ['UpdateMediaCategory', 'umc'])

    def updateMediaCategory(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                mediaInfo = text[len(args[0])+1:].strip().capitalize()
                if mediaInfo:
                    mediaID, categoryID = parseUtils.parseMediaCategory_update(mediaInfo)
                    sqlResult = adapter.update_MediaCategory(mediaID, categoryID)
                    if not sqlResult:
                        mName = adapter.getMediaNameByID(mediaID)
                        cName = adapter.getMediaCategoryByID(categoryID)
                        slackUtils.inChannelResponse(client, channel, comments.updateMediaCategory.format(mName, cName))
                        return
                    slackUtils.inChannelResponse(client, channel, comments.notFound3)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)    
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(UpdateMediaCategory())

class UpdateMediaType(Command):
    def __init__(self):
        super().__init__(source = UpdateMediaType, method = self.updateMediaType, name = ['UpdateMediaType', 'umt'])

    def updateMediaType(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                mediaInfo = text[len(args[0])+1:].strip().capitalize()
                if mediaInfo:
                    mediaID, typeID = parseUtils.parseMediaType_update(mediaInfo)
                    sqlResult = adapter.update_MediaType(mediaID, typeID)
                    if not sqlResult:
                        mName = adapter.getMediaNameByID(typeID)
                        cName = adapter.getMediaTypeByID(typeID)
                        slackUtils.inChannelResponse(client, channel, comments.updateMediaType.format(mName, cName))
                        return
                    slackUtils.inChannelResponse(client, channel, comments.notFound3)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)    
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(UpdateMediaType())

class AdminCheckOut(Command):
    def __init__(self):
        super().__init__(source = AdminCheckOut, method = self.checkout, name = ['AdminCheckOut', 'aco'])

    def checkout(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                mediaInfo = text[len(args[0])+1:].strip().capitalize()
                if mediaInfo:
                    mID, sID = parseUtils.parseAdminCheckout(mediaInfo)
                    exists = adapter.getMediaNameByID(mID)
                    if exists:
                        sanitary = parseUtils.sanitizeID(sID)
                        sqlResult = adapter.Media_adminCheckOUT(mID, sanitary)
                        if sqlResult == 5:
                            slackUtils.inChannelResponse(client, channel, comments.checkedOUT.format(exists))
                            return
                        slackUtils.inChannelResponse(client, channel, comments.doesntExist)
                        return
                    slackUtils.inChannelResponse(client, channel, comments.notEnough)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(AdminCheckOut())

class AdminCheckIn(Command):
    def __init__(self):
        super().__init__(source = AdminCheckIn, method = self.checkin, name = ['AdminCheckIn', 'aci'])

    def checkin(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                someID = text[len(args[0])+1:].strip()
                if someID:
                    exists = adapter.getMediaNameByID(someID)
                    if exists != -1 and exists:
                        sqlResult = adapter.Media_adminCheckIN(someID)
                        if not sqlResult:
                            slackUtils.inChannelResponse(client, channel, comments.adminCheckIN.format(exists))
                            return
                        slackUtils.inChannelResponse(client, channel, comments.notFound3)
                        return
                    slackUtils.inChannelResponse(client, channel, comments.doesntExist)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(AdminCheckIn())

class PutBack(Command):
    def __init__(self):
        super().__init__(source = PutBack, method = self.putBack, name = ['Return'])

    def putBack(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                args = text.split()
                someID = text[len(args[0])+1:].strip()
                if someID:
                    sanitary = parseUtils.sanitizeID(someID)
                    try:
                        borrowed = adapter.getMyStuff(sanitary)
                        exists = adapter.returnAll(sanitary)
                        formatted = parseUtils.parseOtherStuff(borrowed)
                        if not exists:
                            returnMsg = comments.allback.format(parseUtils.reconstitueID(sanitary)) + formatted + "It needs to be put back.\n" + comments.returnItem 
                            slackUtils.inChannelResponse(client, channel, returnMsg)
                            return
                    except:
                        slackUtils.inChannelResponse(client, channel, comments.what3)
                        return
                    slackUtils.inChannelResponse(client, channel, comments.doesntExist)
                    return
                slackUtils.inChannelResponse(client, channel, comments.what)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(PutBack())

class WhoTookIt(Command):
    def __init__(self):
        super().__init__(source = WhoTookIt, method = self.getWhoTookIt, name = ['WhoTookIt', 'taken'])

    def getWhoTookIt(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        #text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                allMedia = adapter.format_Media_WhosGotIt()
                parsed = parseUtils.parseMedia_WhosGotIt(allMedia)
                slackUtils.inChannelResponse(client, channel, parsed)
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)

published.append(WhoTookIt())

########################
###  Admin Template  ###
########################

class AdminTemplate(Command):
    def __init__(self):
        super().__init__(source = AdminTemplate, method = self.templateFunction, name = ['AddFact', 'addf'])

    def templateFunction(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        #text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isAdmin(aUser):
            if adapter.isDirect(client, channel):
                #doStuff
                return
            slackUtils.inChannelResponse(client, channel, comments.notDirect)
            return
        slackUtils.inChannelResponse(client, channel, comments.notAdmin)