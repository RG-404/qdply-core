name="b"
subdomain_preexist=`cat /Users/rishi/projects/qdply-core/nginx-config/qdply \
| grep b.qdply.com`
n=${#subdomain_preexist}
echo $n