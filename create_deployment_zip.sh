# create_deployment_zip.sh -- Creates a zip archive of app files.
#
# Inputs: It will include all files from the web/ subdirectory.
# Outputs: It will create or update the file "petitions_mapview_deploy.zip".
cd `dirname $0`
outfile=petitions_mapview_deploy.zip
if [ -f $outfile ]; then
  rm $outfile
fi
cd web
find -type f | grep -v '.*.swp$' | xargs zip -r ../$outfile
echo "Created deployment zip: $outfile"
