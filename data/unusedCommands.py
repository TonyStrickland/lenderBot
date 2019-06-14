############################
###   !updateMediaType   ###
############################

# if command.startswith("!updateMediaType".lower()):
# 	if adapter.isAdmin(aUser):
# 		if adapter.isDirect(channel):
# 			mediaInfo = command[len("!updateMediaType")+1:].strip().title()
# 			if mediaInfo:
# 				typeID, newType = parseMediaType_update(mediaInfo)
# 				newType = newType.title()
# 				sqlResult = adapter.update_MediaType(typeID, newType)
# 				if not sqlResult:
# 					inChannelResponse(channel, updateMediaType.format(typeID, newType))
# 					return
# 				inChannelResponse(channel, notFound3)
# 				return
# 			inChannelResponse(channel, what)
# 			return
# 		inChannelResponse(channel, notDirect)
# 		return
# 	inChannelResponse(channel, notAdmin)
# 	return

################################
###   !updateMediacategory   ###
################################

# if command.startswith("!updateMediacategory".lower()):
# 	if adapter.isAdmin(aUser):
# 		if adapter.isDirect(channel):
# 			mediaInfo = command[len("!updateMediacategory")+1:].strip().title()
# 			if mediaInfo:
# 				typeID, newType = parseMediaCategory_update(mediaInfo)
# 				newType = newType.title()
# 				sqlResult = adapter.update_MediaCategory(typeID, newType)
# 				if not sqlResult:
# 					inChannelResponse(channel, updateMediaCategory.format(typeID, newType))
# 					return
# 				inChannelResponse(channel, notFound3)
# 				return
# 			inChannelResponse(channel, what)
# 			return
# 		inChannelResponse(channel, notDirect)
# 		return
# 	inChannelResponse(channel, notAdmin)
# 	return