#!/usr/bin/env python

import imp, os, sys, platform

here = os.path.dirname( os.path.abspath( __file__ ) )
chFilePath = os.path.join( os.path.dirname( here ) , "common", "CompileHelper.py" )
try:
  fd = open( chFilePath )
except Exception, e:
  print "Cannot open %s: %s" % ( chFilePath, e )
  sys.exit( 1 )

chModule = imp.load_module( "CompileHelper", fd, chFilePath, ( ".py", "r", imp.PY_SOURCE ) )
fd.close()
chClass = getattr( chModule, "CompileHelper" )

ch = chClass( here )

versions = { 'rrdtool' : "1.2.27" }
ch.setPackageVersions( versions )

if not ch.downloadPackage( "rrdtool" ):
  ch.ERROR( "Could not download rrdtool" )
  sys.exit( 1 )

if not ch.unTarPackage( "rrdtool" ):
  ch.ERROR( "Could not deploy rrdtool" )
  sys.exit( 1 )

prefix = ch.getPrefix()
env = {}
env[ 'CC' ] = 'gcc'
env[ 'LDFLAGS' ] = "-L%s" % os.path.join( prefix, "lib" )
env[ 'CPPFLAGS' ] = ""
ch.setDefaultEnv( env )
includeDirs = ( "", "freetype2", "libart-2.0" )
for dir in includeDirs:
  env[ 'CPPFLAGS' ] += "-I%s " % os.path.join( prefix, "include", dir )

configFlags = []
configFlags.append( "--enable-static" )
configFlags.append( "--disable-shared" )
configFlags.append( "--disable-python" )
configFlags.append( "--disable-ruby" )
configFlags.append( "--disable-perl" )
configFlags.append( "--disable-tcl" )
if not ch.deployPackage( "rrdtool", configureArgs = " ".join( configFlags ) ):
  ch.ERROR( "Could not deploy rrdtool" )
  sys.exit( 1 )
