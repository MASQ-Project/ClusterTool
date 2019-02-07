# Copyright (c) 2019, Substratum LLC (https://substratum.net) and/or its affiliates. All rights reserved.
from traffic import Traffic

EXIT_CODES = [
    "Success",
    "Unsupported protocol. This build of curl has no support for this protocol.",
    "Failed to initialize.",
    "URL malformed. The syntax was not correct.",
    "A feature or option that was needed to perform the desired request was not enabled or was explicitly disabled at build-time. To make curl able to do this, you probably need another build of libcurl!",
    "Couldn't resolve proxy. The given proxy host could not be resolved.",
    "Couldn't resolve host. The given remote host was not resolved.",
    "Failed to connect to host.",
    "FTP weird server reply. The server sent data curl couldn't parse.",
    "FTP access denied. The server denied login or denied access to the particular resource or directory you wanted to reach. Most often you tried to change to a directory that doesn't exist on the server.",
    "FTP weird PASS reply. Curl couldn't parse the reply sent to the PASS request.",
    "FTP weird PASV reply, Curl couldn't parse the reply sent to the PASV request.",
    "FTP weird 227 format. Curl couldn't parse the 227-line the server sent.",
    "FTP can't get host. Couldn't resolve the host IP we got in the 227-line.",
    "FTP couldn't set binary. Couldn't change transfer method to binary.",
    "Partial file. Only a part of the file was transferred.",
    "FTP couldn't download/access the given file, the RETR (or similar) command failed.",
    "FTP quote error. A quote command returned error from the server.",
    "HTTP page not retrieved. The requested url was not found or returned another error with the HTTP error code being 400 or  above.  This  return  code  only appears if -f, --fail is used.",
    "Write error. Curl couldn't write data to a local filesystem or similar.",
    "FTP couldn't STOR file. The server denied the STOR operation, used for FTP uploading.",
    "Read error. Various reading problems.",
    "Out of memory. A memory allocation request failed.",
    "Operation timeout. The specified time-out period was reached according to the conditions.",
    "FTP PORT failed. The PORT command failed. Not all FTP servers support the PORT command, try doing a transfer using PASV instead!",
    "FTP couldn't use REST. The REST command failed. This command is used for resumed FTP transfers.",
    "HTTP range error. The range \"command\" didn't work.",
    "HTTP post error. Internal post-request generation error.",
    "SSL connect error. The SSL handshaking failed.",
    "FTP bad download resume. Couldn't continue an earlier aborted download.",
    "FILE couldn't read file. Failed to open the file. Permissions?",
    "LDAP cannot bind. LDAP bind operation failed.",
    "LDAP search failed.",
    "Function not found. A required LDAP function was not found.",
    "Aborted by callback. An application told curl to abort the operation.",
    "Internal error. A function was called with a bad parameter.",
    "Interface error. A specified outgoing interface could not be used.",
    "Too many redirects. When following redirects, curl hit the maximum amount.",
    "Unknown option specified to libcurl. This indicates that you passed a weird option to curl that was passed on to libcurl and rejected. Read up in the manual!",
    "Malformed telnet option.",
    "The peer's SSL certificate or SSH MD5 fingerprint was not OK.",
    "The server didn't reply anything, which here is considered an error.",
    "SSL crypto engine not found.",
    "Cannot set SSL crypto engine as default.",
    "Failed sending network data.",
    "Failure in receiving network data.",
    "Problem with the local certificate.",
    "Couldn't use specified SSL cipher.",
    "Peer certificate cannot be authenticated with known CA certificates.",
    "Unrecognized transfer encoding.",
    "Invalid LDAP URL.",
    "Maximum file size exceeded.",
    "Requested FTP SSL level failed.",
    "Sending the data requires a rewind that failed.",
    "Failed to initialise SSL Engine.",
    "The user name, password, or similar was not accepted and curl failed to log in.",
    "File not found on TFTP server.",
    "Permission problem on TFTP server.",
    "Out of disk space on TFTP server.",
    "Illegal TFTP operation.",
    "Unknown TFTP transfer ID.",
    "File already exists (TFTP).",
    "No such user (TFTP).",
    "Character conversion failed.",
    "Character conversion functions required.",
    "Problem with reading the SSL CA cert (path? access rights?).",
    "The resource referenced in the URL does not exist.",
    "An unspecified error occurred during the SSH session.",
    "Failed to shut down the SSL connection.",
    "Could not load CRL file, missing or wrong format (added in 7.19.0).",
    "Issuer check failed (added in 7.19.0).",
    "The FTP PRET command failed",
    "RTSP: mismatch of CSeq numbers",
    "RTSP: mismatch of Session Identifiers",
    "unable to parse FTP file list",
    "FTP chunk callback reported error",
    "No connection available, the session will be queued",
    "SSL public key does not matched pinned public key",
]


class Curl(Traffic):
    def __init__(self, site, executor):
        self.site = site
        self.p = executor(self._command())
        self.done = False
        self.result = ""

    def status(self):
        if self.done: # we were already done and queried
            return self.result

        if self.p.isalive(): # we are still executing
            return "curl %s is still waiting for a response" % self.site

        # we finished since the last status check
        self.done = True

        # add exit code info
        if self.p.exitstatus < len(EXIT_CODES):
            self.result = "curl %s (%i: %s)" % (self.site, self.p.exitstatus, EXIT_CODES[self.p.exitstatus])
        else:
            self.result = "curl %s (%i: unknown)" % (self.site, self.p.exitstatus)

        # add pass/fail info
        if self.p.exitstatus == 0:
            self.result = "%s %s" % (self.result, "SUCCEEDED")
        else:
            self.result = "%s %s" % (self.result, "FAILED")

        return self.result

    def cleanup(self, executor):
        self.p.terminate(force=True)

    def _command(self):
        return ["curl", "-s", self.site]
