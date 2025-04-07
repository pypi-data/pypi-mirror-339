# Pacote Poetry brseclabcripto

## Instalação

```console
pip install brseclabcripto
```

## Uso

### Importar biblioteca

```console
from brseclabcripto import cripto2
```

### Gerar chave

```python
key = cripto2.generate_aes_key()
```

### Criptografar string

```python
ciphertext = cripto2.aes_gcm_encrypt(key,"TEXTO")
```

### Decriptar

```python
decriptado = cripto2.aes_gcm_decrypt(key,ciphertext)
```

### Gerar hash com argon2id

```python
hash_argon = hash_argon2id(key,password)
```

### Verificar hash argon2id

```python
hash_argon2id_verify(hash_argon, key,password)
```
