#!/bin/bash

createopen(){
    if [ ! -d "/tmp/$1" ] ; then
        read -sp "Informe a chave de criptografia: " PASSWORD
        echo ""
        if [ ! -f "/home/$SUDO_USER/$1.img" ] ; then
            read -p "Informe o tamanho em GB (exemplo 1 para 1GB): " LENGTH
            echo ""
            if ! [[ "$LENGTH" =~ ^[1-9][0-9]*$ ]] ; then
                echo "Tamanho inválido (informe um inteiro positivo em GB)."
                return 1
            fi
            dd if=/dev/urandom of="/home/$SUDO_USER/$1.img" bs=1M count=$(( LENGTH * 1024 ))
            printf 'YES\n%s\n%s\n' "$PASSWORD" "$PASSWORD" | /usr/sbin/cryptsetup luksFormat "/home/$SUDO_USER/$1.img"
            echo -n "$PASSWORD" | /usr/sbin/cryptsetup open --type luks "/home/$SUDO_USER/$1.img" "$1"
            mkfs.ext4 -L "$1" "/dev/mapper/$1"
            /usr/sbin/cryptsetup close "$1"
        fi
        echo -n "$PASSWORD" | /usr/sbin/cryptsetup open --type luks "/home/$SUDO_USER/$1.img" "$1"
        mkdir "/tmp/$1"
        mount "/dev/mapper/$1" "/tmp/$1"
        if findmnt "/tmp/$1" > /dev/null; then
            chown -R "$SUDO_USER:$SUDO_USER" "/tmp/$1/"
        else
            rm -r "/tmp/$1"
        fi

    else
        echo "Já está aberto"
    fi
}
#1 = nome do arquivo
createopen $1

# REFERENCIA:
#https://serverfault.com/questions/513605/how-to-non-interactively-supply-a-passphrase-to-dmcrypt-luksformat
#https://opensource.com/article/21/4/linux-encryption