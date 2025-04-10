import os
import sys
import ssl
import tempfile
import socket 
import ipaddress
import logging
import base64
import zlib

from datetime import (datetime, 
					  timedelta)

from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from urllib.parse import urlparse
from typing import Any

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

logging = logging.getLogger('app.dbms.cert')

from ..logic import Logic
from .config import Config
from .key import Key

class Crt(Logic):

	trusted = bool()

	__padding = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
							 algorithm=hashes.SHA256(),
							 label=None)

	def __init__(self, key: str, 
					   value: Any = None, 
					   pattern: str = 'default', **kwargs):
		if pattern != None:
			self.pattern = pattern
		if key and abs(self) and 'https://' in key:
			if key := urlparse(key).netloc:
				try:
					crt = ssl.get_server_certificate((key, 443))
				except:
					pass
				else:
					value = crt.encode()
		if not self.key and key != None and value != None:
			self.key, self.value = (str(key)[:512], value); self.save()
		elif self.key and not self.value and value != None:
			self.update(value)

	def __enter__(self):
		return self

	@property
	def tmp(self, tmp = None):
		if tmp := tempfile.NamedTemporaryFile(prefix=self.key, dir='/dev/shm' if sys.platform.startswith('linux') else None, suffix='.crt', delete=True, mode='wb+'):
			tmp.write(self.value.encode() if isinstance(self.value, str) else self.value); tmp.seek(0);
		return tmp

	@classmethod
	def url(cls, url):
		try:
			parser = urlparse(url)
		except:
			pass
		else:
			if parser.netloc:
				try:
					crt = ssl.get_server_certificate((parser.netloc, 443))
				except:
					pass
				else:
					return url, parse.netloc, crt.encode()


	@classmethod
	def __new__(cls, *args, **kwargs):
		if len(args) == 2 and args[1] is not None and 'https://' in args[1]:
			try:
				args[1] = urlparse(args[1]).netloc
			except:
				pass
		if _ := cls.__hex__(args[1], **kwargs) if len(args) == 2 else None:
			if object := cls.__(_):
				return object
		return super().__new__(cls)

	@property
	def rsa(self):
		if crt := x509.load_pem_x509_certificate(self.value.encode() if isinstance(self.value, str) else self.value):
			return crt.public_key()

	def encrypt(self, input: bytes, size:int = 256, offset:int = 0, _ = bytes()) -> bytes:
		if input := zlib.compress(input):
			while not offset >= len(input):
				if chunk := input[offset:offset + size]:
					if len(chunk) % size != 0:
						chunk += bytes(bytearray((size - len(chunk))))
					_ += self.rsa.encrypt(chunk, self.__padding); offset += size
		return base64.b64encode(_)

	def verify(self, input: bytes, signature: bytes) -> bool:
		try:
			self.public.verify(
					data=input.encode() if isinstance(input, str) else pickle.dumps(input),
					signature=signature,
					padding=padding.PSS(
						mgf=padding.MGF1(hashes.SHA256()),
						salt_length=padding.PSS.MAX_LENGTH
					),
					algorithm=hashes.SHA256())
		except InvalidSignature:
			return False
		else:
			return True
		return False

	@classmethod
	def create(
		cls,
		hostname: str,
		ip: tuple = (),
		key: object = None
	) -> object:
		""" If certyficate exists, return old one.
		"""
		if crt := cls(hostname):
			return crt
		"""
		Generate a self-signed X509 certificate.
		:param hostname:  Must provide a hostname
		:param public_ip:  Can optionally provide a public IP
		:param private_ip:  Can optionally provide a private IP
		:return: A tuple of the certificate PEM and the key PEM

			'BUSINESS_CATEGORY', 'COMMON_NAME', 'COUNTRY_NAME', 'DN_QUALIFIER', 
			'DOMAIN_COMPONENT', 'EMAIL_ADDRESS', 'GENERATION_QUALIFIER', 'GIVEN_NAME', 
			'INN', 'JURISDICTION_COUNTRY_NAME', 'JURISDICTION_LOCALITY_NAME', 
			'JURISDICTION_STATE_OR_PROVINCE_NAME', 'LOCALITY_NAME', 'OGRN', 
			'ORGANIZATIONAL_UNIT_NAME', 'ORGANIZATION_NAME', 'POSTAL_ADDRESS', 
			'POSTAL_CODE', 'PSEUDONYM', 'SERIAL_NUMBER', 'SNILS', 'STATE_OR_PROVINCE_NAME', 
			'STREET_ADDRESS', 'SURNAME', 'TITLE', 'UNSTRUCTURED_NAME', 'USER_ID', 
			'X500_UNIQUE_IDENTIFIER'
		"""
		issuer = name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, hostname),
						  x509.NameAttribute(NameOID.COUNTRY_NAME, u'US'),
						  x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'CA'),
						  x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
						  x509.NameAttribute(NameOID.ORGANIZATION_NAME, u're:lock'),
						  x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'Self signed certyficate'),
						  x509.NameAttribute(NameOID.EMAIL_ADDRESS, u'no-reply@relock.id'),
						  x509.NameAttribute(NameOID.SERIAL_NUMBER, str(x509.random_serial_number())),
						  x509.NameAttribute(NameOID.GIVEN_NAME, hostname)])
		
		# Setup our alt names.
		alt_names_list = [
			# Best practice seem to be to include the hostname in the SAN, which *SHOULD* mean COMMON_NAME is ignored.
			x509.DNSName(hostname)
		]

		# Allow addressing by IP, for when you don't have real DNS (common in most testing scenarios)
		for _ in list(ip):
			if ip := socket.gethostbyname(_):
				logging.info('append alt_name for %s on %s', hostname, _)
				# openssl wants DNSnames for ips...
				alt_names_list.append(x509.DNSName(hostname))
				# ... whereas golang's crypto/tls is stricter, and needs IPAddresses
				alt_names_list.append(x509.IPAddress(ipaddress.IPv4Address(_)))

		san = x509.SubjectAlternativeName(alt_names_list)

		# ca=True, path_len=0 means this cert can only sign itself, not other certs.
		basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
		key_usage = x509.KeyUsage(digital_signature=True, key_encipherment=True, key_cert_sign=True,
								  key_agreement=True, content_commitment=False, data_encipherment=False,
								  crl_sign=False, encipher_only=False, decipher_only=False)
		extended_key_usage = x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.SERVER_AUTH])
		subject_key = x509.SubjectKeyIdentifier.from_public_key(key._public)
		authority_key = x509.AuthorityKeyIdentifier.from_issuer_public_key(key._public)


		if now := datetime.utcnow():
			cert = (
				x509.CertificateBuilder()
				.subject_name(name)
				.issuer_name(name)
				.public_key(key._public)
				.serial_number(x509.random_serial_number())
				.not_valid_before(now)
				.not_valid_after(now + timedelta(days=10 * 365))
				.add_extension(basic_contraints, False)
				.add_extension(san, False)
				.add_extension(key_usage, True)\
				.add_extension(extended_key_usage, False)\
				.add_extension(subject_key, False)
				.add_extension(authority_key, False)
				.sign(key._private, hashes.SHA256(), default_backend())
			)
		logging.info('Certyficate created for %s -> %s', hostname, ip)
		return cls(hostname, cert.public_bytes(encoding=serialization.Encoding.PEM))

	def delete(self):
		if self and self.trusted:
			if sys.platform.startswith('darwin'):
				if job := self.job('sudo', 'security', 'delete-certificate', '-c', self.key, '/Library/Keychains/System.keychain'):
					print(job)
					if not job.stderr:
						logging.info('REMOVE Certyficate from System, this can\'t be reversed')
			if sys.platform.startswith('linux'):
				if file := '/usr/local/share/ca-certificates/%s.crt' % self.key:
					if os.path.isfile(file):
						if job := self.job('update-ca-certificates', '--fresh'):
							if not job.stderr:
								logging.info('REMOVE Certyficate from System, this can\'t be reversed')
			if config := Config('%s.serial' % self.key):
				if config.delete():
					if config := Config('%s.fingerprint' % self.key):
						config.delete()
		return super().delete()

	# HOST=gmail-pop.l.google.com
	# PORT=995

	# openssl s_client -servername $HOST -connect $HOST:$PORT < /dev/null 2>/dev/null | openssl x509 -outform pem > scylla.crt

	def trust(self):
		if not self.trusted:
			with tempfile.NamedTemporaryFile(prefix=self.key, suffix='.crt', delete=True, mode='wb+') as crt:
				crt.write(self.value.encode() if isinstance(self.value, str) else self.value); crt.seek(0);
				if sys.platform.startswith('darwin'):
					self.osx(crt.name)
				elif sys.platform.startswith('linux'):
					self.linux(crt.name, self.key)
				self.trusted = True
				self.update()
		return self.trusted

	def osx(self, file):
		try:
			os.popen("sudo security authorizationdb write com.apple.trust-settings.admin allow ; sudo security add-trusted-cert -p ssl -d -r trustRoot -k /Library/Keychains/System.keychain %s ; sudo security authorizationdb remove com.apple.trust-settings.admin" % file).read()
		except:
			raise SystemError('Trust authorization of certyficate faild. %s' % self.delete())
		else:
			if serial := os.popen('openssl x509 -noout -serial -sha1 -in %s | xargs | cut -d= -f2' % file).read().strip():
				if Config('%s.serial' % self.key, serial):
					if fingerprint := os.popen('openssl x509 -noout -fingerprint -sha1 -in %s | xargs | cut -d= -f2' % file).read().strip():
						if Config('%s.fingerprint' % self.key, fingerprint):
							pass
		finally:
			logging.debug('Certyficate is trusted.')

	def linux(self, file, hostname: str = None):
		try:
			if crt := '/usr/local/share/ca-certificates/%s.crt' % (hostname or str(self)):
				#openssl x509 -inform PEM -in /usr/local/share/ca-certificates/root2022.cer -out /usr/local/share/ca-certificates/certificate.crt
				if job := self.job('openssl', 'x509', '-in', file, '-out', crt):
					if not job.stderr:
						if serial := os.popen('openssl x509 -noout -serial -sha1 -in %s | xargs | cut -d= -f2' % crt).read().strip():
							if Config('%s.serial' % self.key, serial):
								if fingerprint := os.popen('openssl x509 -noout -fingerprint -sha1 -in %s | xargs | cut -d= -f2' % crt).read().strip():
									if Config('%s.fingerprint' % self.key, fingerprint):
										if job := self.job('chmod', '644', crt):
											if not job.stderr:
												if job := self.job('update-ca-certificates', '--fresh'):
													for line in job.stdout.decode().split('\n'):
														if line != 'done.':
															logging.info(line)
													if not job.stderr:
														logging.info('Certyficate import to System, success.')

		except:
			raise SystemError('Trust authorization of certyficate faild. %s' % self.delete(hostname))
		finally:
			logging.notify('Certyficate is trusted.')