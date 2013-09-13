# -*- coding: utf-8 -*-
"""Public Controller"""
from biorepo.lib.base import BaseController
from tg import expose, flash, redirect, response, url
from biorepo.model import DBSession, Files_up, Measurements
from biorepo.lib.constant import dico_mimetypes
import os
from biorepo.lib.util import check_boolean
import socket
from sqlalchemy import and_

__all__ = ['PublicController']


class PublicController(BaseController):

    @expose()
    def public_link(self, sha1, *args, **kw):
        f = DBSession.query(Files_up).filter(Files_up.sha1 == sha1).first()
        #if used with BAM_visualisation
        if f is None:
            tmp = sha1.split('.')
            sha1 = tmp[0]
            f = DBSession.query(Files_up).filter(Files_up.sha1 == sha1).first()

        path_fu = f.path + "/" + f.sha1
        extension = f.extension
        filename = f.filename
        file_size = os.path.getsize(path_fu)
        if dico_mimetypes.has_key(extension):
            response.content_type = dico_mimetypes[extension]
        else:
            response.content_type = 'text/plain'
        response.headers['X-Sendfile'] = path_fu
        response.headers['Content-Disposition'] = 'attachement; filename=%s' % (filename)
        response.content_length = '%s' % (file_size)
        return None

    @expose()
    def BAM_visualisation(self, bam_object, filename_without_extension, *args, **kw):
        #find the bam.bai file associated
        bai = DBSession.query(Files_up).filter(and_(Files_up.filename == filename_without_extension + ".bam.bai", Files_up.extension == "bai")).first()
        if bai is None:
            flash("Sorry but " + bam_object.filename + " has no .bam.bai associated in BioRepo. Upload it and retry the operation.", "error")
            raise redirect(url("/search"))
        else:
            bai_sha1 = bai.sha1
            bam_sha1 = bam_object.sha1
            bai_path = bai.path
            bam_path = bam_object.path
            #build the full paths (bam and bam.bai)
            bai_full_path = bai_path + "/" + bai_sha1
            bam_full_path = bam_path + "/" + bam_sha1
            #creating symlink with good names and good extensions
            #for the bam file
            bam_dest = bam_path + "/" + bam_sha1 + ".bam"
            os.symlink(bam_full_path, bam_dest)
            bam_name = bam_sha1 + ".bam"
            #for the bai file
            bai_dest = bam_path + "/" + bam_sha1 + ".bam.bai"
            os.symlink(bai_full_path, bai_dest)
            return bam_name

    @expose()
    def UCSC_link(self, sha1, meas_id, t, *args, **kw):
        #URL example
        #http://genome.ucsc.edu/cgi-bin/hgTracks?org=mouse&hgt.customText=http://yoururl.com/tracks.txt&db=mm9&position=chr4:107816815-107817581
        assemblies_Org = {'mm8': 'mouse', 'mm9': 'mouse', 'saccer2': 'yeast'}
        meas = DBSession.query(Measurements).filter(Measurements.id == meas_id).first()
        list_a_values = []
        #get the dynamic values
        for val in meas.a_values:
            list_a_values.append(val.id)
        #check if "assembly" is a dynamic key for this measurement
        cpt_test = 0
        for a in meas.attributs:
            if a.key == "assembly":
                cpt_test += 1
                #get all the values recorded for this key
                list_assemblies = a.values
                assembly = ''
                for v in list_assemblies:
                    #check if the Attributs_values object is linked to this measurement
                    if v.id in list_a_values:
                        assembly = v.value
                if assembly == '':
                    flash("Sorry but you have to set an assembly to this measurement", "error")
                    raise redirect("/search")

                elif assembly.lower() in assemblies_Org.keys():
                    org = assemblies_Org[assembly.lower()]
                    hostname = socket.gethostname().lower()
                    if int(t) == 1:
                        raise redirect('http://genome.ucsc.edu/cgi-bin/hgTracks?org=' + org + "&hgt.customText=http://" + hostname + url("/public/public_link?sha1=") + sha1 + "&db=" + assembly)
                    elif int(t) == 2:
                        ext2type = {'bb': 'bigBed', 'bw': 'bigWig'}
                        f = DBSession.query(Files_up).filter(Files_up.sha1 == sha1).first()
                        e = f.extension
                        fullname = f.filename
                        name_tmp = fullname.split('.')
                        name = name_tmp[0]
                        if e in ext2type.keys():
                            extension = ext2type[e]
                        else:
                            flash(str(e) + " : extension not known", "error")
                            raise redirect("/search")
                        #URL example in UCSC API
                        #http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg18&position=chr21:33038447-33041505&hgct_customText
                        #=track%20type=bigBed%20name=myBigBedTrack%20description=%22a%20bigBed%20track%22%20visibility=
                        #full%20bigDataUrl=http://genome.ucsc.edu/goldenPath/help/examples/bigBedExample.bb
                        raise redirect('http://genome.ucsc.edu/cgi-bin/hgTracks?db=' + assembly + "&hgct_customText=track%20type=" + extension +
                                        "%20name=" + name + "%20bigDataUrl=http://" + hostname + url("/public/public_link?sha1=") + sha1)
                    elif int(t) == 3:
                        #1)detect if .bai for this .bam with filename.split('.')
                        #2)create 2 symlink with same name and the 2 extensions (.bam and .bai)
                        #3)give the public path of the .bam symlink (create a UCSC-bam-visu(self, bam_filename))
                        #4)delete them ? (when ? how ?)
                        bam_file = DBSession.query(Files_up).filter(Files_up.sha1 == sha1).first()
                        fullname = bam_file.filename
                        name_tmp = fullname.split('.')
                        name = name_tmp[0]
                        bam_name = self.BAM_visualisation(bam_file, name)
                        raise redirect('http://genome.ucsc.edu/cgi-bin/hgTracks?db=' + assembly + "&hgct_customText=track%20type=bam" +
                                        "%20name=" + name + "%20bigDataUrl=http://" + hostname + url("/public/public_link?sha1=") + bam_name)

                else:
                    flash("Sorry, the assembly is not known by BioRepo. Contact your administrator please.", "error")
                    raise redirect("/search")
        if cpt_test == 0:
            flash("oups error", "error")
            raise redirect("/search")



