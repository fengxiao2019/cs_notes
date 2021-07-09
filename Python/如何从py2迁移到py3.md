如何从py2迁移到py3
[https://slack.engineering/migrating-slack-airflow-to-python-3-without-disruption/][1]
slack的工程师分享了将airflow从py2迁移到py3的过程，非常详细，做一下笔记。
规模：上百个DAGs
步骤：
1. **Set up a virtual environment**: Created a working Python 3 virtual environment with Airflow and all the dependencies.
2. **Set up Python 3 workers**: Launched Python 3 celery workers running the virtual environment from step 1, and make them pick tasks from a “python3” queue on Redis.
3. **Clean up phase 1**: Removed stale or unused DAGs to make the migration easier.
4. **Fix Python 3 incompatibilities in DAGs**: Updated DAGs to be Python 2/3 compatible but let them continue to run on Python 2 workers.
5. **Move the DAGs to Python 3 workers**: Tested and switched DAGs from Python 2 to Python 3 workers. We started with a small set and kept increasing depending on success rate. If DAGs failed, we fixed forward or rolled back to Python 2 workers.
6. **Migrate the Airflow services to Python 3**: Switched web server, scheduler, and flower to Python 3.
7. **Clean up phase 2**: Cleaned up Python 2 references and virtual environments, and terminated Python 2 celery workers.

现在开发环境做，测试完全通过后，再在生产环境部署。
使用到的工具：
automatic Python 2 to 3 converters: 2to3 and futurize. 
Use Poetry for dependency management of Python 2 and 3:
pyenv 虚拟环境管理
详细细节见原文

[1]:	https://slack.engineering/migrating-slack-airflow-to-python-3-without-disruption/