# Sieve
The Sieve package and Python client. See the [Sieve Documentation](https://docs.sievedata.com/guide/intro) for usage information.

## Integration Tests
Push your local client package branch
```
# sieve
git checkout -b newbranch
git push -u origin newbranch
```

Now push to server repository to start the ci
- make typecheck will fail
```
# server
git checkout -b newbranch
git commit --allow-empty -m "Trigger Build"
git push -u origin newbranch
```

Make a pr, add a comment with "/pulmi"; it will create infra for testing. Pulumi action takes a little while. When it's done, a CI context should be created. You might get unrelated errors, if you do rerun the CI

When it goes thru, go to the context

	https://app.circleci.com/settings/organization/github/sieve-data/contexts

Delete `SIEVE_WHEEL_NAME` and then replace the value with a different wheel name (as to not break dev release), e.g.
```
SIEVE_WHEEL_NAME: “sievedata-mybranch-filenone-py3-none-any.whl”
```

Now push client package again. `Run Tests` fail sometimes, as long as `build_push` passes you are good.




