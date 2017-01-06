from __future__ import absolute_import
import os
from cleaner.tag import Tag


class DockerProject(object):
    """A project within a docker registry"""

    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]

    @property
    def tagfiles(self):
        if not hasattr(self, '_tagfiles'):
            self._tagfiles = filter(lambda tf: tf.startswith('tag_'),
                                    os.listdir(self.path))
        return self._tagfiles

    @property
    def environments(self):
        if not hasattr(self, '_envs'):
            self._envs = {t.environment for t in self.flat_tags}
            if None in self._envs:
                self._envs.add('Hash')
                self._envs.remove(None)
        return self._envs

    @property
    def flat_tags(self):
        if not hasattr(self, '_flattags'):
            self._flattags = []
            for tf in self.tagfiles:
                p = '/'.join([self.path, tf])
                self._flattags.append(Tag(p))
        return self._flattags

    def tags(self, environment):
        def ekey(t):
            return t.environment
        if not hasattr(self, '_tags'):
            result = {}
            sorted_tags = sorted(self.flat_tags, key=ekey)
            for env_name, group in groupby(sorted_tags, key=ekey):
                env_name = 'Hash' if env_name is None else env_name
                result[env_name] = sorted([tag for tag in group], reverse=True)
            self._tags = result
        return self._tags.get(environment, [])

    def old_deploy_tags(self, cutoff):
        """cutoff: unix time for oldest allowable tag"""
        old = []

        for env in self.environments:
            if env == 'Hash':
                continue
            env_tags = self.tags(env)

            # always keep the 10 latest tags for an environment
            possible_discard = env_tags[10:]
            too_old = next((x for x in possible_discard
                            if x.mtime < cutoff), None)
            if too_old is not None:
                idx = possible_discard.index(too_old)
                old.extend(possible_discard[idx:])
        return old

    def old_hash_tags(self, cutoff, deploy_tags_to_remove):
        """cutoff: unix time for oldest allowable tag"""

        ts = self.tags('Hash')[10:]
        # We keep the 10 latest
        if not ts:
            return []

        whitelist = ['latest']

        # Filter tags that are too old and not whitelisted
        old = [t for t in ts
               if t.mtime < cutoff and t.tag not in whitelist]

        old_and_unreferenced = []
        for tag in old:
            img = tag.image

            # the set of all tags with image == this tag's image except this
            hash_tags_referencing_img = {t for t in self.flat_tags
                                         if t.image == img and t != tag} - set(deploy_tags_to_remove)

            if not any(hash_tags_referencing_img):
                old_and_unreferenced.append(tag)

        return old_and_unreferenced
