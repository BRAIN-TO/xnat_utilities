import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    
    #fieldmap different echo...
    #add more information
    
    #MPRAGE:
    t1w_mprage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MPRAGE_run-{item:02d}_T1w')
    t1w_mp2rage = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-MP2RAGE_run-{item:02d}_T1w')
    
    #T1w:
    #t1w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_run-{item:02d}_T1w')
    
    #T2w:
    spc_T2w = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_T2w')
    
    #FLAIR:
    spc_FLAIR = create_key('{bids_subject_session_dir}/anat/{bids_subject_session_prefix}_acq-SPACE_run-{item:02d}_FLAIR')
    
    #BOLD:
    bold = create_key('{bids_subject_session_dir}/func/{bids_subject_session_prefix}_task-{task}_dir-{dir}_run-{item:02d}_bold')
    
    #Perfusion:
    asl = create_key('{bids_subject_session_dir}/perf/{bids_subject_session_prefix}_run-{item:02d}_asl')
    perfusion = create_key('{bids_subject_session_dir}/perf/{bids_subject_session_prefix}_run-{item:02d}_perfusion')
    
    #Diffusion:
    dwi = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_dwi')
    dwi_FA = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_FA')
    dwi_TENSOR = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_TENSOR')
    dwi_TENSORB0 = create_key('{bids_subject_session_dir}/dwi/{bids_subject_session_prefix}_run-{item:02d}_TENSORB0')
    
    #Field Maps:
    fmap_diff = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_part-phase_MEGRE')
    fmap_magnitude = create_key('{bids_subject_session_dir}/fmap/{bids_subject_session_prefix}_part-mag_MEGRE')
    
    #extra:
    extra = create_key('{bids_subject_session_dir}/extra/{bids_subject_session_prefix}_acq-{acq}_run-{item:02d}_extra')
    localizer = create_key('{bids_subject_session_dir}/extra/{bids_subject_session_prefix}_localizer')
    
    
    info = {t1w_mprage: [], spc_T2w: [], spc_FLAIR: [], bold: [], asl: [], perfusion: [], dwi: [], dwi_FA: [], dwi_TENSOR: [], dwi_TENSORB0: [], fmap_diff: [], fmap_magnitude: [], extra: [], localizer: []}
    # last_run = len(seqinfo)

    for idx, s in enumerate(seqinfo):
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """
        #Field Maps
        if ('FIELDMAPPING' in s.protocol_name) or ('fieldmapping' in s.protocol_name):   
            if (s.dim4 == 1) and (('GRE_FIELDMAPPING' in (s.series_description).strip()) or ('gre_fieldmapping' in (s.series_description).strip())):
                if('P' in (s.image_type[2].strip()) ):
                    info[fmap_diff].append(s.series_id)
                    continue
                if('M' in (s.image_type[2].strip()) ):
                    info[fmap_magnitude].append(s.series_id)
                    continue
        
        #MPRAGE
        if (('mprage' in s.protocol_name) or ('T1w' in s.protocol_name) or ('MPRAGE' in s.protocol_name)):
                info[t1w_mprage].append(s.series_id)
                continue
            
        #MP2RAGE
        if (('mp2rage' in s.protocol_name) or ('MP2RAGE' in s.protocol_name)) and (not 'memp2rage' in s.series_description):
                if ('T1' in (s.series_description).strip()):
                    info[t1w_mp2rage].append(s.series_id)
                    continue
        
        #spc T2w-improve later
        if ('SPACE-T2' in s.series_description or 'space-T2' or 'T2w_SPC' in s.series_description or 'T2w_space' in s.series_description or 't2_space' in s.series_description or 't2_spc' in s.series_description or 'T2_spc' in s.series_description.strip() ): 
            if ('ND' in s.series_description):
                info[extra].append({'item':s.series_id, 'acq': s.protocol.name})
                continue
            else:
                info[spc_T2w].append(s.series_id)
                continue
        
        #spc T2w FLAIR
        if ('SPACE-FLAIR' in s.series_description): 
            if ('ND' in s.series_description):
                info[extra].append({'item':s.series_id, 'acq': s.protocol.name})
                continue
            else:
                info[spc_FLAIR].append(s.series_id)
                continue
        
        #BOLD
        if ('BOLD' in s.series_description) and ('FMRI' in (s.image_type[2].strip())):
            if ('PA' in (s.series_description).strip()):
                info[bold].append({'item': s.series_id, 'task': 'rest', 'dir':'PA'})
                continue
            elif ('AP' in (s.series_description).strip()):
                info[bold].append({'item': s.series_id, 'task': 'rest', 'dir':'AP'})
                continue
            
        #Perfusion
        if ('ASL' in (s.image_type[2].strip())):
            if ('ORIGINAL' in (s.image_type[0].strip())):
                info[asl].append(s.series_id)
                continue
            elif ('DERIVED' in (s.image_type[0].strip())) and ('SUBTRACTION' in (s.image_type[3].strip())):
                info[perfusion].append(s.series_id)
                continue
        
        #dwi
        if ('DIFFUSION' in (s.image_type[2].strip())) or ('DTI'in (s.series_description).strip()) or ('DWI' in (s.series_description).strip()):
            if ('ORIGINAL' in (s.image_type[0].strip())):
                info[dwi].append(s.series_id)
                continue
            elif ('DERIVED' in (s.image_type[0].strip())):
                if ('FA' in (s.image_type[3].strip())):
                    info[dwi_FA].append(s.series_id)
                    continue
                elif ('TENSOR' in (s.image_type[3].strip())):
                    info[dwi_TENSOR].append(s.series_id)
                    continue
                elif ('TENSOR_B0' in (s.image_type[3].strip())):
                    info[dwi_TENSORB0].append(s.series_id)
                    continue     
                
        if ('localizer' in (s.series_description)) or ('LOCALIZER' in (s.series_description)):
            info[localizer].append(s.series_id)
                
        info[extra].append({'item': s.series_id, 'acq': s.protocol.name})
    
    
        
        

    return info
