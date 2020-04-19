from btpeer import *

PEERNAME = "NAME"
LISTPEERS = "LIST"
INSERTPEER = "JOIN"
QUERY = "QUER"
QRESPONSE = "RESP"
FILEGET = "FGET"
PEERQUIT = "QUIT"
REPLY = "REPL"
ERROR = "ERRO"


class FilerPeer(BTPeer):
	def __init__(self, maxpeers, serverport):
		BTPeer.__init__(self, maxpeers, serverport)
		self.files = {}
		self.addrouter(self.__router)
		handlers = {LISTPEERS : self.__handle_listpeers,
					INSERTPEER : self.__handle_insertpeer,
					PEERNAME : self.__handle_peername,
					QUERY : self.__handle_query,
					QRESPONSE : self.__handle_qresponse,
					FILEGET : self.__handle_fileget,
					PEERQUIT : self.__handle_quit}
		for mt in handlers:
			self.addhandler(mt, handlers[mt])

	def __router(self, peerid):
		if peerid not in self.getpeerids():
			return (None, None, None)
		else:
			rt = [peerid]
			rt.extend(self.peers[peerid])
			return rt

	def __handle_insertpeer(self, peerconn, data):
		self.peerlock.acquire()
		try:
			try:
				peerid, host, port = data.split()

				if self.maxpeersreached():
					self.__debug('max peers %d reached: connection terminating'
									% self.maxpeers)
					peerconn.senddata(ERROR, 'Join: too many peers')
					return

				if peerid not in self.getpeerids() and peerid != self.myid:
					self.addpeer(peerid, host, port)
					self.__debug('added peer: %s' % peerid)
					peerconn.senddata(REPLY, 'Join: peer added: %s' % peerid)
				else:
					peerconn.senddata(ERROR, 'Join: peer already inserted %s'
										% peerid)
			except:
				print('invalid insert %s: %s' % (str(peerconn), data))
		finally:
			self.peerlock.release()

	def __handle_listpeers(self, peerconn, data):
		self.peerlock.acquire()
		try:
			print('Listing peers %d' % self.numberofpeers())
			peerconn.senddata(REPLY, '%d' % self.numberofpeers())
			for pid in self.getpeerids():
				host,port = self.getpeer(pid)
				peerconn.senddata(REPLY, '%s %s %d' % (pid, host, port))
		finally:
			self.peerlock.release()

	def __handle_peername(self, peerconn, data):
		peerconn.senddata(REPLY, self.myid)

	def __handle_query(self, peerconn, data):
		try:
			peerid, key, ttl = data.split()
			peerconn.senddata(REPLY, 'Query ACK: %s' % key)
		except:
			print('invalid query %s: %s' % (str(peerconn), data))
			peerconn.senddata(ERROR, 'Query: incorrect arguments')

		t = threading.Thread(target = self.__processquery,
								args = [peerid, key, int(ttl)])
		t.start()

	def __processquery(self, peerid, key, ttl):
		for fname in self.files.keys():
			if key in fname:
				fpeerid = self.files[fname]
				if not fpeerid:
					fpeerid = self.myid
				host,port = peerid.split(':')
				self.connectandsend(host, int(port), QRESPONSE,
										'%s %s' % (fname, fpeerid),
										pid = peerid)
				return
		if ttl > 0:
			msgdata = '%s %s %d' % (peerid, key, ttl - 1)
			for nextpid in self.getpeerids():
				self.sendtopeer(nextpid, QUERY, msgdata)

	def __handle_qresponse(self, peerconn, data):
		try:
			fname, fpeerid = data.split()
			if fname in self.files:
				self.__debug('Cant add duplicate file %s %s' %
								(fname, fpeerid))
			else:
				self.files[fname] = fpeerid
		except:
			traceback.print_exc()

	def __handle_fileget(self, peerconn, data):
		fname = data
		if fname not in self.files:
			print('File not found %s' % fname)
			peerconn.senddata(ERROR, 'File not found')
			return
		try:
			fd = file(fname, 'r')
			filedata = ''
			while True:
				data = fd.read(2048)
				if not len(data):
					break
				filedata += data
			fd.close()
		except:
			print('Error reading file %s' % fname)
			peerconn.senddata(ERROR, 'Error reading file')
			return
		peerconn.senddata(REPLY, filedata)

	def __handle_quit(self, peerconn, data):
		self.peerlock.acquire()
		try:
			peerid = data.lstrip().rstrip()
			if peerid in self.getpeerids():
				msg = 'Quit: peer removed: %s' % peerid
				print(msg)
				peerconn.senddata(REPLY, msg)
				self.removepeer(peerid)
			else:
				msg = 'Quit: peer not found: %s' % peerid
				print(msg)
				peerconn.senddata(ERROR, msg)
		finally:
			self.peerlock.release()

	def buildpeers(self, host, port, hops = 1):
		if self.maxpeersreached() or not hops:
			return

		peerid = None

		print("Building peers from (%s,%s)" % (host, port))

		try:
			_, peerid = self.connectandsend(host, port, PEERNAME, '')[0]
			self.__debug("contacted " + peerid)
			resp = self.connectandsend(host,port,INSERTPEER,
										'%s %s %d' % (self.myid, 
														self.serverhost,
														self.serverport))[0]
			self.__debug(str(resp))
			if (resp[0] != REPLY) or (peerid in self.getpeerids()):
				return

			self.addpeer(peerid, host, port)

			resp = self.connectandsend(host, port, LISTPEERS, '',
										pid = peerid)
			if len(resp) > 1:
				resp.reverse()
				resp.pop()
				while len(resp):
					nextpid, host, port = resp.pop()[1].split()
					if nextpid != self.myid:
						self.buildpeers(host, port, hops - 1)
		except:
			print("error build peers")
			self.removepeer(peerid)

	def addlocalfile(self, filename):
		self.files[filename] = None
		print("Added local file %s" % filename)
