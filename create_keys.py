import rsa

if __name__ == '__main__':
    public, private = rsa.newkeys(512)

    with open("my_key.pub", "wb") as file:
        file.write(public.save_pkcs1())

    with open("my_key.prv", "wb") as file:
        file.write(private.save_pkcs1())
