$ErrorActionPreference = 'Stop'
$toolsDir = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$packageName = 'azgelir'
$url = 'https://github.com/Tamerefe/AzGelir/releases/download/v1.0.0/AzGelir_Setup.exe'

$packageArgs = @{
  packageName   = $packageName
  unzipLocation = $toolsDir
  fileType      = 'EXE'
  url           = $url
  silentArgs    = '/S'
  validExitCodes= @(0)
  softwareName  = 'AzGelir*'
  checksum      = ''
  checksumType  = 'sha256'
}

Install-ChocolateyPackage @packageArgs