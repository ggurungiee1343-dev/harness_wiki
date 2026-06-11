처음 `sudo ln -s ...` 한 번만 실행하면 심링크가 생성됩니다. 그 다음부터는 그냥:

- `switch-model got` 
- `switch-model deepseek`

이렇게만 입력하면 됩니다. 매번 전체 경로 칠 필요 없어요.

**한 번만 실행:**
```bash
sudo ln -s ~/Applications/venu/scripts/switch_model.sh /usr/local/bin/switch-model
```

**이후 사용:**
```bash
switch-model got        # GPT-OSS-120B 전환
switch-model deepseek   # DeepSeek 전환
```

심링크가 안 될 경우를 대비한 원본 직접 실행 코드도 알려드리자면:
```bash
~/Applications/venu/scripts/switch_model.sh got
~/Applications/venu/scripts/switch_model.sh deepseek
```

이것도 똑같이 동작합니다. 심링크 성공 여부와 상관없이 위 원본 경로로 직접 실행해도 됩니다.