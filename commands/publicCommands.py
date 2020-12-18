
import Conan.slackUtils as slackUtils
from Conan.slackUtils import Command as Command
import Conan.parseUtils as parseUtils
import Conan.lendingLibraryAdapter as adapter
import Conan.data.comments as comments

published = []

def ParsePayload(payLoad):
    web_client = payLoad['web_client']
    data = payLoad['data']
    channel = data['channel']
    user = data['user']
    text = data['text']
    return web_client, data, channel, user, text

class Fact(Command):
    def __init__(self):
        super().__init__(source = Fact, method = self.giveFact, name = ['Fact'])

    def giveFact(self, payLoad):
        # TODO generate a random Conan fact
        return

class Insult(Command):
    def __init__(self):
        super().__init__(source = Insult, method = self.giveInsult, name = ['Insult'])

    def giveInsult(self, payLoad):
        # TODO generate a random Conan fact
        return      

class Help(Command):
    def __init__(self):
        super().__init__(source = Help, method = self.giveHelp, name = ['Help', '?'])

    def giveHelp(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        aUser = payLoad['data']['user']
        slackUtils.inChannelResponse(client, channel, comments.cromHelp)
        if adapter.isAdmin(aUser):
            slackUtils.directResponse(client, channel, aUser, comments.adminHelp)
            return
        slackUtils.directResponse(client, channel, aUser, comments.publicHelp)

published.append(Help())

class Who(Command):
    def __init__(self):
        super().__init__(source = Who, method = self.tellWho, name = ['Who'])

    def tellWho(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        aUser = payLoad['data']['user']
        slackUtils.inChannelResponse(client, channel, comments.conanTells)  
        slackUtils.directResponse(client, channel, aUser, comments.aboutConan)

published.append(Who())

###########################
###   DIRECT commands   ###
###########################

class AllMediaCategories(Command):
    def __init__(self):
        super().__init__(source = AllMediaCategories, method = self.tellAll, name = ['allMediaCategories', 'amc'])

    def tellAll(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        if adapter.isDirect(client, channel):
            allCategory = adapter.selectAll_MediaCategory()
            parsed = parseUtils.parseMediaCategory_select(allCategory)
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(AllMediaCategories())

class AllMediaTypes(Command):
    def __init__(self):
        super().__init__(source = AllMediaTypes, method = self.runAMT, name = ['AllMediaTypes', 'amt'])

    def runAMT(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        if adapter.isDirect(client,channel):
            allCategory = adapter.selectAll_MediaType()
            parsed = parseUtils.parseMediaType_select(allCategory)
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(AllMediaTypes())

class Everything(Command):
    def __init__(self):
        super().__init__(source = Everything, method = self.getEverything, name = ['Everything', 'all'])

    def getEverything(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']      
        if adapter.isDirect(client, channel):
            allMedia = adapter.format_Media()                
            parsed = parseUtils.parseMedia_select(allMedia)
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(Everything())

class Avialable(Command):
    def __init__(self):
        super().__init__(source = Avialable, method = self.getAvailable, name = ['Available'])

    def getAvailable(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        if adapter.isDirect(client, channel):
            allMedia = adapter.format_Media_Available()                
            parsed = parseUtils.parseMedia_select(allMedia)
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(Avialable())

class ViewCategory(Command):
    def __init__(self):
        super().__init__(source = ViewCategory, method = self.getByCategory, name = 'ViewCategory')

    def getByCategory(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        if adapter.isDirect(client, channel):
            args = text.split()
            if len(args) < 2:
                slackUtils.inChannelResponse(client, channel, comments.badCommand)
                return
            mediaInfo = args[1].strip().title()
            sqlResult = adapter.getAvalableByCategory(mediaInfo)
            if sqlResult:
                parsed = parseUtils.parseViewMediaByCategory(sqlResult)
                parsed = comments.viewCategoryInfo.format(mediaInfo) + parsed
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(ViewCategory())

class ViewType(Command):
    def __init__(self):
        super().__init__(source = ViewType, method = self.getByType, name = 'ViewType')

    def getByType(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        if adapter.isDirect(client, channel):
            args = text.split()
            if len(args) < 2:
                slackUtils.inChannelResponse(client, channel, comments.badCommand)
                return
            mediaInfo = args[1].strip().title()
            sqlResult = adapter.getAvalableByCategory(mediaInfo)
            if sqlResult:
                parsed = parseUtils.parseViewMediaByCategory(sqlResult)
                parsed = comments.viewCategoryInfo.format(mediaInfo) + parsed
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(ViewType())

class MyStuff(Command):
    def __init__(self):
        super().__init__(source = MyStuff, method = self.getMyStuff, name = ['MyStuff', 'Mine'])

    def getMyStuff(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        aUser = payLoad['data']['user']
        if adapter.isDirect(client, channel):
            allMedia = adapter.getMyStuff(aUser)
            parsed = parseUtils.parseMyStuff(allMedia)
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(MyStuff())

class CheckOut(Command):
    def __init__(self):
        super().__init__(source = CheckOut, method = self.doCheckout, name = ['CheckOut', 'CO'])

    def doCheckout(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.getSlackName(aUser) == 'No ID':
            adapter.addUser(client.users_info(user = aUser)['user'])
        if adapter.isDirect(client, channel):
            args = text.split()
            if len(args) < 2:
                slackUtils.inChannelResponse(client, channel, comments.badCommand)
                return
            someID = args[1].strip()
            if someID:
                exists = adapter.getMediaNameByID(someID)
                if exists != -1 and exists:

                    sqlResult = adapter.Media_CheckOUT(someID, aUser)
                    if sqlResult == 5:
                        slackUtils.inChannelResponse(client, channel, comments.checkedOUT.format(exists))
                        return
                    if sqlResult == 4:
                        slackUtils.inChannelResponse(client, channel, comments.noGreed)
                        return
                    if not sqlResult:
                        slackUtils.inChannelResponse(client, channel, comments.takeIt.format(exists))
                        return
                    slackUtils.inChannelResponse(client, channel, comments.checkedOUT.format(exists))
                    return
                slackUtils.inChannelResponse(client, channel, comments.doesntExist)
                return
            slackUtils.inChannelResponse(client, channel, comments.correctCheckOUT)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(CheckOut())

class CheckIn(Command):
    def __init__(self):
        super().__init__(source = CheckIn, method = self.doCheckIn, name = ['CheckIn', 'CI'])

    def doCheckIn(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isDirect(client, channel):
            args = text.split()
            if len(args) < 2:
                slackUtils.inChannelResponse(client, channel, comments.badCommand)
                return
            someID = args[1].strip()
            if someID:
                exists = adapter.getMediaNameByID(someID)
                if exists != -1 and exists:
                    sanatary = parseUtils.sanitizeID(aUser)
                    sqlResult = adapter.Media_CheckIN(someID, sanatary)
                    if sqlResult == 3:
                        slackUtils.inChannelResponse(client, channel, comments.notYou.format(exists))
                        return
                    if sqlResult == 5:
                        slackUtils.inChannelResponse(client, channel, comments.checkedOUT.format(exists))
                        return
                    if not sqlResult:
                        slackUtils.inChannelResponse(client, channel, comments.bringIt.format(exists))
                        return
                    slackUtils.inChannelResponse(client, channel, comments.notTaken.format(exists))
                    return
                slackUtils.inChannelResponse(client, channel, comments.doesntExist)
                return
            slackUtils.inChannelResponse(client, channel, comments.correctCheckOUT)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(CheckIn())

class SearchMedium(Command):
    def __init__(self):
        super().__init__(source = SearchMedium, method = self.doLookup, name = ['SearchMedium', 'sm'])

    def doLookup(self, payLoad):
        client = payLoad['web_client']
        channel = payLoad['data']['channel']
        text = payLoad['data']['text']
        aUser = payLoad['data']['user']
        if adapter.isDirect(client, channel):
            args = text.split()
            if len(args) < 2:
                slackUtils.inChannelResponse(client, channel, comments.badCommand)
                return
            medium = args[1].strip()
            if medium:
                exists = adapter.returnMedium(medium)
                if exists != -1 and exists:
                    sqlResult = adapter.returnMedium(medium)
                    if sqlResult == 3:
                        slackUtils.inChannelResponse(client, channel, comments.notYou.format(exists))
                        return
                    if sqlResult == 5:
                        slackUtils.inChannelResponse(client, channel, comments.checkedOUT.format(exists))
                        return
                    if not sqlResult:
                        slackUtils.inChannelResponse(client, channel, comments.bringIt.format(exists))
                        return
                    slackUtils.inChannelResponse(client, channel, comments.notFound2.format(exists))
                    return
                slackUtils.inChannelResponse(client, channel, comments.doesntExist)
                return
            slackUtils.inChannelResponse(client, channel, comments.correctCheckOUT)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

#Keeping disabled until testing completed
#published.append(SearchMedium())