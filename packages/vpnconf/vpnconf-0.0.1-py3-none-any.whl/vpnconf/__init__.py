import argparse
import os
import zipfile

def read_file(name):
    cwd = os.getcwd()
    path = os.path.join(cwd, name)
    with open(path, encoding='utf-8') as f:
        return f.read()

def cert_and_key(paths):
    path1, path2 = paths
    ext1 = os.path.splitext(path1)[1]
    ext2 = os.path.splitext(path2)[1]
    if ext1 == '.crt' or ext2 == '.key':
        return path1, path2
    if ext2 == '.crt' or ext1 == '.key':
        return path2, path1
    return path1, path2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--ca", required=True)
    parser.add_argument("--cert", nargs=2, required=True)
    parser.add_argument("--ta", required=True)
    parser.add_argument("-o", "--output", required=True)

    args = parser.parse_args()

    output = args.output
    ext = os.path.splitext(args.output)[1]

    cert_path, key_path = cert_and_key(args.cert)

    name = os.path.splitext(os.path.basename(cert_path))[0]

    ca = read_file(args.ca)
    ta = read_file(args.ta)
    cert = read_file(cert_path)
    key = read_file(key_path)

    if ext == '.ovpn':
        with open(output, "w", encoding='utf-8') as f:
            print(f"""client
dev tun
remote {args.host}
disable-dco
<ca>
{ca}
</ca>
<cert>
{cert}
</cert>
<key>
{key}
</key>
<tls-auth>
{ta}
</tls-auth>
key-direction 1
""", file = f)
    elif ext == '.zip':
        with open(f"{name}.conf", "w", encoding='utf-8') as f:
            print(f"""client
dev tun
remote {args.host}
ca ca.crt
cert {os.path.basename(cert_path)}
key {os.path.basename(key_path)}
tls-auth ta.key 1
""", file = f)
        if os.path.exists(output):
            os.remove(output)
        with zipfile.ZipFile(output, 'w') as z:
            for path in [f"{name}.conf", args.ca, args.ta, cert_path, key_path]:
                z.write(path, arcname=os.path.basename(path))

if __name__ == "__main__":
    main()