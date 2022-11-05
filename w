      conn.send(str.encode(cmd))
            respone_size += 20000
            print("****************************WARNING**********************************")
            print("[RESPONSE SIZE]...", 'Current Max Bytes for This Response : ', respone_size, "....")
            print('Keep your Eye ...', 'This Response is Constantly updating by 20,000 Bytes per a single request: ',
                  respone_size)
            print("****************************WARNING**********************************")
            line += 1
            client_response = str(conn.recv(respone_size), 'utf-8')
            img_file_name = input(('Response : ', client_response, "line : ", line))
            conn.send(str.encode(img_file_name))
            save_img = str(conn.recv(80000), 'utf-8')
            # save_img = bytes.decode(save_img)
            print('recied')
            save_img = bytes(save_img,'utf-8')
            print(save_img, type(save_img))
            if img_file_name[-3:] == "JPG":
                exe = "jpg"
                img_file_name = img_file_name[:-3]
                fw_j = open(path + "/" + img_file_name + exe, 'wb')
                for line_j in save_img:
                    fw_j.write(line_j)
                    fw_j.close()
            else:
                exe = "png"
                img_file_name = img_file_name[:-3]
                fw_p = open(dn + "/" + img_file_name + exe, 'wb')
                for line_p in save_img:
                    fw_p.write(bytes(line_p))
                    fw_p.close()
            print('op')

            print('------FILE SUCCESSFULLY SAVED AS ' + cmd + "---------")
