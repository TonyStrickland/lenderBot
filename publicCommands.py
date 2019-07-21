import lendingLibraryAdapter
import slackUtils
import lendingLibraryAdapter as adapter
import comments

published = []

class Command():
    def __init__(self, source, method, name, **kwargs):
        self.method = method
        self.source = source
        self.name = name
        self.kwargs = kwargs

def ParsePayload(payLoad):
    web_client = payLoad['web_client']
    data = payLoad['data']
    channel = data['channel']
    user = data['user']
    text = data['text']
    return web_client, data, channel, user, text

class SayHello(Command):
    def __init__(self):
        super().__init__(source = SayHello, method = self.say_hello, name = ["Hello", 'h'])

    def say_hello(self, payLoad):
        thread_ts = None
        client, data, channel, user, text = ParsePayload(payLoad)
        if 'thread_ts' in payLoad:
            thread_ts = payLoad['thread_ts']
        if client is not None and len(text) > 0:
            message_args = {
                'channel' : channel,
                'text' : 'Hello!',
                'as_user' : True
            }       
            if thread_ts is not None:
                message_args['thread_ts'] = thread_ts   
        client.chat_postMessage(**message_args)

published.append(SayHello())

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
        client, data, channel, aUser, text = ParsePayload(payLoad)
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
        client, data, channel, aUser, text = ParsePayload(payLoad)
        slackUtils.inChannelResponse(client, channel, comments.conanTells)  
        slackUtils.directResponse(client, channel, aUser, comments.aboutConan)

published.append(Who())

class AllMediaCategories(Command):
    def __init__(self):
        super().__init__(source = AllMediaCategories, method = self.tellAll, name = ['allMediaCategories', 'amc'])

    def tellAll(self, payLoad):
        client, data, channel, aUser, text = ParsePayload(payLoad)
        if adapter.isDirect(channel):
            allCategory = adapter.selectAll_MediaCategory()
            parsed = slackUtils.parseMediaCategory_select(allCategory)
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(AllMediaCategories())

class AllMediaTypes(Command):
    def __init__(self):
        super().__init__(source = AllMediaTypes, method = self.runAMT, name = ['AllMediaTypes', 'amt'])

    def runAMT(self, payLoad):
        client, data, channel, aUser, text = ParsePayload(payLoad)
        if adapter.isDirect(channel):
            allCategory = adapter.selectAll_MediaType()
            parsed = slackUtils.parseMediaType_select(allCategory)
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(AllMediaTypes())

class Everything(Command):
    def __init__(self):
        super().__init__(source = Everything, method = self.getEverything, name = ['Everything', 'all'])

    def getEverything(self, payLoad):
        client, data, channel, aUser, text = ParsePayload(payLoad)
        if adapter.isDirect(channel):
            allMedia = adapter.format_Media()                
            parsed = slackUtils.parseMedia_select(allMedia)
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(Everything())

class Avialable(Command):
    def __init__(self):
        super().__init__(source = Avialable, method = self.getAvailable, name = ['Available'])

    def getAvailable(self, payLoad):
        client, data, channel, aUser, text = ParsePayload(payLoad)
        if adapter.isDirect(channel):
            allMedia = adapter.format_Media_Available()                
            parsed = slackUtils.parseMedia_select(allMedia)
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(Avialable())

class ViewCategory(Command):
    def __init__(self):
        super().__init__(source = ViewCategory, method = self.getByCategory, name = 'ViewCategory')

    def getByCategory(self, payLoad):
        client, data, channel, aUser, text = ParsePayload(payLoad)
        if adapter.isDirect(channel):
            args = text.split()
            if len(args) < 2:
                slackUtils.inChannelResponse(client, channel, comments.badCommand)
                return
            mediaInfo = args[1].strip().title()
            sqlResult = adapter.getAvalableByCategory(mediaInfo)
            if sqlResult:
                parsed = slackUtils.parseViewMediaByCategory(sqlResult)
                parsed = comments.viewCategoryInfo.format(mediaInfo) + parsed
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(ViewCategory())

class ViewType(Command):
    def __init__(self):
        super().__init__(source = ViewType, method = self.getByType, name = 'ViewType')

    def getByType(self, payLoad):
        client, data, channel, aUser, text = ParsePayload(payLoad)
        if adapter.isDirect(channel):
            args = text.split()
            if len(args) < 2:
                slackUtils.inChannelResponse(client, channel, comments.badCommand)
                return
            mediaInfo = args[1].strip().title()
            sqlResult = adapter.getAvalableByCategory(mediaInfo)
            if sqlResult:
                parsed = slackUtils.parseViewMediaByCategory(sqlResult)
                parsed = comments.viewCategoryInfo.format(mediaInfo) + parsed
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(ViewType())

class MyStuff(Command):
    def __init__(self):
        super().__init__(source = MyStuff, method = self.getMyStuff, name = ['MyStuff', 'Mine'])

    def getMyStuff(self, payLoad):
        client, data, channel, aUser, text = ParsePayload(payLoad)
        if adapter.isDirect(channel):
            allMedia = adapter.getMyStuff(aUser)
            parsed = slackUtils.parseMyStuff(allMedia)
            slackUtils.inChannelResponse(client, channel, parsed)
            return
        slackUtils.inChannelResponse(client, channel, comments.notDirect)

published.append(MyStuff())

class CheckOut(Command):
    def __init__(self):
        super().__init__(source = CheckOut, method = self.doCheckout, name = ['CheckOut', 'CO'])

    def doCheckout(self, payLoad):
        client, data, channel, aUser, text = ParsePayload(payLoad)
        if adapter.isDirect(channel):
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
        client, data, channel, aUser, text = ParsePayload(payLoad)
        if adapter.isDirect(channel):
            args = text.split()
            if len(args) < 2:
                slackUtils.inChannelResponse(client, channel, comments.badCommand)
                return
            someID = args[1].strip()
            if someID:
                exists = adapter.getMediaNameByID(someID)
                if exists != -1 and exists:
                    sanatary = slackUtils.sanitizeID(aUser)
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

published.append(CheckOut())